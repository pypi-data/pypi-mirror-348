from databricks.sdk.runtime import *
from delta.tables import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from datetime import datetime

def delta_merge(df, pk_col, delta_table, is_scd_key_filter=False, is_update_filter=False):
    merge_condition = " AND ".join([f"target.{col} = updates.{col}" for col in pk_col]) + \
                      " AND target.effective_to is null AND target.record_status = 'A'" + \
                      (" AND target.scd_key = updates.scd_key" if is_scd_key_filter else "")

    update_condition = "target.upd_key != updates.upd_key" if is_update_filter else None

    when_matched_update_column_dictionary = {
        f"{column}": f"updates.{column}"
        for column in (set(df.columns) - {"dw_inserted_at", "effective_from"})
    }

    when_not_matched_insert_column_dictionary = {
        f"{column}": f"updates.{column}"
        for column in df.columns
    }

    delta_table.alias("target").merge(
        df.alias("updates"),
        merge_condition
    ).whenMatchedUpdate(
        condition=update_condition, set=when_matched_update_column_dictionary
    ).whenNotMatchedInsert(values=when_not_matched_insert_column_dictionary).execute()
    last_operation_df = delta_table.history(1)
    display(last_operation_df.select("operationMetrics"))


def implement_scd2(df, scd_key_col, pk_col, target_table, select_col_list=None, effective_from_col=None, initial_eff_date=None):
    target_df = (
        spark.sql(f"select * from {target_table}")
        .withColumn("effective_to", coalesce(col("effective_to"), current_timestamp()))
        .withColumn("row_number", row_number().over(Window.partitionBy(*pk_col).orderBy(col("dw_inserted_at").desc(), col("effective_to").desc())))
        .filter(col("row_number") == 1)
    )

    delta_table = DeltaTable.forName(spark, target_table)

    scd_cols = ["record_status", "effective_from", "effective_to", "dw_inserted_at", "dw_updated_at", "scd_key", "upd_key"]
    select_cols_list = [col for col in select_col_list if col not in scd_cols] if select_col_list else df.columns

    updates_hashkey_col = [col for col in select_cols_list if col not in scd_key_col and col not in scd_cols]
    scd_key_col.extend([col for col in pk_col if col not in scd_key_col])

    current_ts = lit(datetime.now())
    effective_from_ts = col(effective_from_col).cast("timestamp") if effective_from_col else current_ts
    initial_effective_from_ts = col(initial_eff_date).cast("date") if initial_eff_date else effective_from_ts

    active_data_df = (
        df.withColumn("record_status", lit("A"))
        .withColumn("effective_from", coalesce(effective_from_ts, current_ts))
        .withColumn("initial_effective_from", coalesce(initial_effective_from_ts, current_ts))
        .withColumn("effective_to", lit(None))
        .withColumn("dw_inserted_at", current_ts)
        .withColumn("dw_updated_at", current_ts)
        .withColumn("scd_key", sha2(concat_ws("", *[col(c) for c in scd_key_col]), 256))
        .withColumn("upd_key", sha2(concat_ws("", *[col(c) for c in updates_hashkey_col]), 256))
        .selectExpr(*select_cols_list, *scd_cols, "initial_effective_from")
    )

    processed_data = (
        active_data_df.alias("active_df").join(
            target_df.alias("target_df"),
            on=pk_col,
            how="inner"
        )
    )

    active_processed_data = processed_data.selectExpr("active_df.*")

    inactive_processed_data_to_update = (
        processed_data.filter("active_df.scd_key != target_df.scd_key")
        .selectExpr("target_df.*", "active_df.effective_from as active_eff_from")
    )

    active_unprocessed_data = (
        active_data_df.alias("active_df").join(
            target_df.alias("target_df"),
            on=pk_col,
            how="left_anti"
        )
        .selectExpr("active_df.*")
        .withColumn("effective_from", col("initial_effective_from"))
    )

    active_union_data_df = (
        active_processed_data
        .unionByName(active_unprocessed_data)
    ).drop("initial_effective_from")

    inactive_data_to_update = (
        inactive_processed_data_to_update.selectExpr(*select_cols_list, "active_eff_from")
        .withColumn("record_status", lit("I"))
        .withColumn("effective_to", col("active_eff_from"))
        .withColumn("dw_inserted_at", current_ts)
        .withColumn("dw_updated_at", current_ts)
        .drop("active_eff_from")
    )

    if inactive_data_to_update.isEmpty() == False:
        delta_merge(inactive_data_to_update, pk_col, delta_table)

    if active_union_data_df.isEmpty() == False:
        delta_merge(active_union_data_df, pk_col, delta_table, is_scd_key_filter=True, is_update_filter=True)