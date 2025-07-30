from pyspark.sql import SparkSession

class PybrvEtlmeta:
    def __init__(self, spark):
        self.spark = spark

    def setup_pybrv_etlmeta(self, database: str):
        """
        Create 'etl_meta' schema and required tables for business rule validation metadata.
        """

        self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {database}.etl_meta")

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_business_rule_check_result (
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
            last_modified_ts TIMESTAMP 
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_data_parity_result (
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
            last_modified_ts TIMESTAMP 
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_metadata (
            unique_rule_identifier INT NOT NULL,
            bookmark_start_date DATE,
            bookmark_end_date DATE,
            last_modified_ts TIMESTAMP 
            
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_unique_rule_mapping (
            unique_rule_identifier BIGINT NOT NULL,
            team_name STRING,
            data_domain STRING,
            rule_category STRING,
            rule_id INT,
            rule_name STRING,
            last_modified_ts TIMESTAMP 
            )
        USING DELTA
        """)

        print(f"✅ Schema {database}.etl_meta and all required tables created successfully.")
