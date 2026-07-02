from pyspark.sql.functions import current_timestamp


class DatabricksBronzeIngestor:

    def __init__(self, spark, source_path, checkpoint_path, target_table):
        self.spark = spark
        self.source_path = source_path
        self.checkpoint_path = checkpoint_path
        self.target_table = target_table

    def run(self):

        df = (
            self.spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "parquet")
            .option("cloudFiles.schemaLocation", self.checkpoint_path)
            .load(self.source_path)
        )

        df = df.withColumn("ingestion_timestamp", current_timestamp())

        query = (
            df.writeStream
            .format("delta")
            .option("checkpointLocation", self.checkpoint_path)
            .outputMode("append")
            .table(self.target_table)
        )

        return query