#this file contains functions supporting various operations encountered on Databricks conversion projects
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
class DatabricksConversionSupplements:
    @staticmethod
    def conform_df_columns(df: DataFrame, new_col_names: list) -> DataFrame:
        if len(new_col_names) != len(df.columns):
            raise ValueError("New column names list must match the number of columns in the DataFrame.")

        renamed_cols = []
        for idx, (old_name, new_name) in enumerate(zip(df.columns, new_col_names)):
            if old_name == new_name:
                renamed_cols.append(df.columns[idx])  # Keep column as-is
            else:
                renamed_cols.append(df.columns[idx] + " AS " + new_name)

        # Build SQL-style select expression to rename only when needed
        exprs = [
            f"`{df.columns[idx]}` AS `{new_col_names[idx]}`" if df.columns[idx] != new_col_names[idx] else f"`{df.columns[idx]}`"
            for idx in range(len(df.columns))
        ]
        
        return df.selectExpr(*exprs)
