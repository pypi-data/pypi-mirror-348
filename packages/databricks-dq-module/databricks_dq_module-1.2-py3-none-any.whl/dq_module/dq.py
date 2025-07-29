from datetime import datetime, timezone
from pyspark.sql import Row
from pyspark.sql.functions import *

class RecordGrowthChecker:
    def __init__(self, spark, audit_table="dq.record_growth_log"):
        self.spark = spark
        self.audit_table = audit_table
        spark.sql(
            f"""
            create table if not exists {self.audit_table} (
                schema string,
                table string,
                prev_count bigint,
                current_count bigint,
                status string,
                message string,
                log_datetime timestamp           
            ) using delta
            """
        )

    def get_previous_count(self, schema, table_name):
        try:
            df = self.spark.table(self.audit_table).filter(f"schema = '{schema}' and table = '{table_name}'")
            latest = df.orderBy("log_datetime", ascending=False).limit(1).collect()
            if latest:
                return latest[0]["current_count"]
            else:
                return None
        except Exception as e:
            print(f"[WARN] Could not read audit log table: {e}")
            return None

    def check_growth(self, schema, table_name):
        current_count = self.spark.table(f"{schema}.{table_name}").count()
        prev_count = self.get_previous_count(schema, table_name)

        status = "PASS"
        message = ""
        if prev_count is None:
            message = "No previous record found. Recording baseline."
        elif current_count > prev_count:
            message = f"Row count increased from {prev_count} to {current_count}."
        else:
            status = "FAIL"
            message = f"Row count did not increase: previous = {prev_count}, current = {current_count}"
            self.log_result(table_name, prev_count or 0, current_count, status, message)
            raise ValueError(f"[DQ FAIL] Row count did not increase: previous = {prev_count}, current = {current_count}")

        self.log_result(schema, table_name, prev_count or 0, current_count, status, message)
        return {"schema": schema, "table": table_name, "status": status, "message": message}

    def log_result(self, schema, table_name, prev_count, current_count, status, message):
        log_df = self.spark.createDataFrame([
            Row(
                schema = schema,
                table = table_name,
                prev_count = prev_count,
                current_count = current_count,
                status = status,
                message = message,
                log_datetime = datetime.now(timezone.utc).isoformat()
            )
        ])

        log_df = log_df.withColumn("log_datetime", to_timestamp(col("log_datetime")))

        log_df.write.mode("append").saveAsTable(self.audit_table)


class NullChecker:
    def __init__(self, spark, audit_table = "dq.null_check_log", fail_on_null = False):
        self.spark = spark
        self.audit_table = audit_table
        self.fail_on_null = fail_on_null # If True, raise error when nulls are found

        spark.sql(
            f"""
            create table if not exists {self.audit_table} (
                schema string,
                table string,
                column string,
                status string,
                null_count bigint,
                message string,
                log_datetime timestamp
            ) using delta
            """
        )

    
    def null_check(self, df, schema, table_name, key_columns):
        null_issues = []
        for column in key_columns:
            null_count = df.filter(col(column).isNull()).count()
            status = "PASS" if null_count == 0 else "FAIL"
            message = (
                f"Column {column} has {null_count} nulls" if null_count > 0
                else f"Column {column} passed null check."
            )
            null_issues.append({
                "schema": schema,
                "table": table_name,
                "column": column,
                "status": status,
                "null_count": null_count,
                "message": message,
                "log_datetime": datetime.now(timezone.utc).isoformat()
            })
        self._log_results(null_issues)

        for res in null_issues:
            if res["status"] == "FAIL" and self.fail_on_null:
                raise ValueError(f"[DQ FAIL] {res['message']}")
        
        df_cleaned = df
        for column in key_columns:
            df_cleaned = df_cleaned.filter(col(column).isNotNull())
        
        return df_cleaned
    
    def _log_results(self, results):
        df = self.spark.createDataFrame([Row(**r) for r in results])
        df = df.withColumn("log_datetime", to_timestamp(col("log_datetime")))
        df.write.mode("append").saveAsTable(self.audit_table)





