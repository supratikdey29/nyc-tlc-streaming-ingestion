from framework.logging.logger import FrameworkLogger


class DatabricksBronzeIngestor:

    def __init__(self, spark, config):

        self.spark = spark

        self.config = config

        self.logger = FrameworkLogger.get_logger(
            "DatabricksBronzeIngestor"
        )

    def ingest(self):

        self.logger.info("Starting Bronze Ingestion")

        self.logger.info(
            "\nBronze Configuration\n"
            f"Source      : {self.config.source.path}\n"
            f"Catalog     : {self.config.target.catalog}\n"
            f"Schema      : {self.config.target.schema_name}\n"
            f"Table       : {self.config.target.table}\n"
            f"Checkpoint  : {self.config.checkpoint.root}\n"
            f"Trigger     : {self.config.streaming.trigger}"
        )          
        
        self.logger.info(
            "Structured Streaming implementation will be added next."
        )