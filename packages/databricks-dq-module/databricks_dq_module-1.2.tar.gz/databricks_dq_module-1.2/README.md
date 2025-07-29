**Version 1.1**

A lightweight PySpark-based data quality (DQ) checking library designed for use in Databricks pipelines.  
It currently supports:

- **Record Growth Check**: Ensure that row counts grow between pipeline runs.
- **Null Check**: Detect and log rows with nulls in key fields.

---

## Installation

Coming soon on PyPI:
```bash
pip3 install databricks-dq-module
```


## Usage

Check taht the row count of a table has increased since the last pipeline run.  
```python
from dq_module.dq import RecordGrowthChecker

checker = RecordGrowthChecker(spark)
result = checker.check_growth("<your_table_name>")
```
This writes audit logs to a Delta table (default: `dq.record_growth_log`).  
Fails the pipeline if no growth is detected.  


Ensure that key fields in a DataFrame are not null, and drop rows that are.  
```python
from dq_module.dq import NullChecker

checker = NullChecker(spark)
df_clean = checker.null_check(<your_df>, "<your_table_name>", ["your", "field"])
```
Logs null stats and drops rows with any nulls in specified columns.  
Writes results to `dq.null_chec_log` table.  