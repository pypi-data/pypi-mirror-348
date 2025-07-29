# Hybrid SCD1 and SCD2 Implementation

This package provides a hybrid implementation of Slowly Changing Dimensions (SCD) Type 1 and Type 2 using Delta Table in Databricks. It allows you to apply SCD2 based on specified columns and SCD1 for other columns.

## Features

1. **Hybrid SCD1 and SCD2**: The code performs a hybrid implementation of SCD1 and SCD2.
2. **Column-based SCD2**: SCD2 will be applied if any value changes in the specified SCD2 columns.
3. **Column-based SCD1**: SCD1 will be applied if any value changes in columns other than the specified SCD2 columns.

## Usage

### apply_scd Function

The `apply_scd` function handles the implementation of SCD based on the specified columns. This function is designed for Delta tables in Databricks and requires the target table to have the following columns: `record_status`, `effective_from`, `effective_to`, `dw_inserted_at`, `dw_updated_at`, `scd_key`, and `upd_key`.

# SCD Handler Example

This example demonstrates how to use the `scd_handler` from the `delta_hybrid_scd` module to apply **Slowly Changing Dimension (SCD) Type 2** logic using PySpark.

## 1. Prepare Data

```python
from datetime import datetime
from delta_hybrid_scd import scd_handler

incremental_data = [
    (1, "Google", 0, "Kite", datetime(2015, 12, 25, 10, 5, 30)),
    (1, "BTC", 0, "Binance", datetime(2016, 12, 25, 11, 5, 30)),
    (3, "ETH", 20, "Binance", datetime(2016, 12, 26, 12, 7, 35))
]

schema = ["id", "stock_name", "balance", "platform", "last_modify_ts"]
df = spark.createDataFrame(incremental_data, schema)
```

## 2. Apply SCD
```python
target_table = f"{catalog_name}.{silver_schema}.account_scd2"
pk_col = ["id", "stock_name"]          # Primary key columns
skey_col = ["balance"]                 # Columns to track SCD2 changes on
effective_from_col = "last_modify_ts"  # Timestamp column to log changes
select_col_list = ["id", "stock_name", "balance", "platform"]

scd_handler.apply_scd(
    df,
    skey_col,
    pk_col,
    target_table,
    select_col_list,
    effective_from_col
)
```