# Hybrid SCD1 and SCD2 Implementation

This package provides a hybrid implementation of Slowly Changing Dimensions (SCD) Type 1 and Type 2 using Delta Table in Databricks. It allows you to apply SCD2 based on specified columns and SCD1 for other columns.

## Features

1. **Hybrid SCD1 and SCD2**: The code performs a hybrid implementation of SCD1 and SCD2.
2. **Column-based SCD2**: SCD2 will be applied if any value changes in the specified SCD2 columns.
3. **Column-based SCD1**: SCD1 will be applied if any value changes in columns other than the specified SCD2 columns.

## Source Code and Instructions

For more details, please visit the [GitHub repository](https://github.com/prateekmshra/delta_lake_platform).