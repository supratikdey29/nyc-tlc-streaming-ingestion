from pipelines.nyc_tlc.bronze.databricks_bronze import DatabricksBronzeIngestor

source_path = "s3://nyc-tlc-tripdata/Green-Trip-data/"
checkpoint_path = "/Volumes/deltalake_dev/checkpoints/checkpoint_loc/green_tripdata"
target_table = "deltalake_dev.nyc_tlc_bronze.green_tripdata"

ingestor = DatabricksBronzeIngestor(
    spark,
    source_path,
    checkpoint_path,
    target_table
)

query = ingestor.run()

query.awaitTermination()