
from pyspark.sql import SparkSession
import argparse

class PybrvEtlmeta:
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()

    def setup_pybrv_etlmeta(self, database: str):
        """
        Create 'etl_meta' schema and required tables for business rule validation metadata.
        """
        
        self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {database}.etl_meta")

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_business_rule_check_result (
            unique_rule_identifier BIGINT,
            execution_id BIGINT,
            team_name VARCHAR(255),
            rule_name VARCHAR(255),
            data_domain VARCHAR(255),
            table_checked VARCHAR(255),
            bookmark_column_name VARCHAR(255),
            bookmark_start_date DATE,
            bookmark_end_date DATE,
            status TEXT,
            pass_record_count INT,
            fail_record_count INT,
            pass_percentage INT,
            threshold INT,
            failed_keys TEXT,
            failed_query TEXT,
            test_case_comments TEXT,
            remarks TEXT,
            last_modified_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_data_parity_result (
            unique_rule_identifier INT,
            execution_id BIGINT,
            rule_name VARCHAR(255),
            data_domain VARCHAR(255),
            table_checked VARCHAR(255),
            bookmark_column_name VARCHAR(255),
            bookmark_column_value DATE,
            join_key_values JSON,
            metric_dim_values JSON,
            attribute_name VARCHAR(255),
            attribute_value INT,
            comments TEXT,
            last_modified_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_metadata (
            unique_rule_identifier INT NOT NULL,
            bookmark_start_date DATE,
            bookmark_end_date DATE,
            last_modified_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT vf_metadata_pkey PRIMARY KEY (unique_rule_identifier)
        )
        USING DELTA
        """)

        self.spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {database}.etl_meta.vf_unique_rule_mapping (
            unique_rule_identifier BIGINT NOT NULL,
            team_name VARCHAR(255),
            data_domain VARCHAR(255),
            rule_category VARCHAR(255),
            rule_id INT,
            rule_name VARCHAR(255),
            last_modified_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT vf_unique_rule_mapping_pkey PRIMARY KEY (unique_rule_identifier)
        )
        USING DELTA
        """)

        print(f"✅ Schema {database}.etl_meta and all required tables created successfully.")

def main():
    parser = argparse.ArgumentParser(description="Create etl_meta schema and tables in Databricks.")
    parser.add_argument("--database", required=True, help="Name of the database/catalog to use")
    args = parser.parse_args()

    creator = PybrvEtlmeta()
    creator.setup_pybrv_etlmeta(args.database)

if __name__ == "__main__":
    main()