from pyspark.sql import SparkSession

class DatabricksPybrvEtlmeta:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def setup_pybrv_etlmeta(self, database: str):
        """
        Create database, 'etl_meta' schema, and required tables for business rule validation metadata.
        """

        # Enable column defaults
        self.spark.sql("SET spark.databricks.delta.properties.defaults.column.defaultValuesSupported = true")

        # Create database and schema
        self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {database}.etl_meta")

        # Drop if exists
        self.spark.sql(f"DROP TABLE IF EXISTS {database}.etl_meta.pybrv_business_rule_check_result")
        self.spark.sql(f"DROP TABLE IF EXISTS {database}.etl_meta.pybrv_data_parity_result")
        self.spark.sql(f"DROP TABLE IF EXISTS {database}.etl_meta.pybrv_metadata")
        self.spark.sql(f"DROP TABLE IF EXISTS {database}.etl_meta.pybrv_unique_rule_mapping")

        # Create tables
        self.spark.sql(f"""
        CREATE TABLE {database}.etl_meta.pybrv_business_rule_check_result (
            unique_rule_identifier BIGINT,
            execution_id BIGINT,
            team_name STRING,
            rule_name STRING,
            data_domain STRING,
            table_checked STRING,
            bookmark_column_name STRING,
            bookmark_start_date DATE,
            bookmark_end_date DATE,
            status STRING,
            pass_record_count INT,
            fail_record_count INT,
            pass_percentage INT,
            threshold INT,
            failed_keys STRING,
            failed_query STRING,
            test_case_comments STRING,
            remarks STRING,
            last_modified_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        USING DELTA
        TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
        """)

        self.spark.sql(f"""
        CREATE TABLE {database}.etl_meta.pybrv_data_parity_result (
            unique_rule_identifier INT,
            execution_id BIGINT,
            rule_name STRING,
            data_domain STRING,
            table_checked STRING,
            bookmark_column_name STRING,
            bookmark_column_value DATE,
            join_key_values STRING,
            metric_dim_values STRING,
            attribute_name STRING,
            attribute_value INT,
            comments STRING,
            last_modified_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        USING DELTA
        TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
        """)

        self.spark.sql(f"""
        CREATE TABLE {database}.etl_meta.pybrv_metadata (
            unique_rule_identifier INT NOT NULL,
            bookmark_start_date DATE,
            bookmark_end_date DATE,
            last_modified_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        USING DELTA
        TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
        """)

        self.spark.sql(f"""
        CREATE TABLE {database}.etl_meta.pybrv_unique_rule_mapping (
            unique_rule_identifier BIGINT NOT NULL,
            team_name STRING,
            data_domain STRING,
            rule_category STRING,
            rule_id INT,
            rule_name STRING,
            last_modified_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        USING DELTA
        TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
        """)

        print(f"✅ All tables in `{database}.etl_meta` created successfully.")
