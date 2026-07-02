from framework.logging.logger import FrameworkLogger
from pipelines.nyc_tlc.bronze.databricks_bronze import DatabricksBronzeIngestor


class BronzePipeline:

    def __init__(self, config, spark=None):
        self.config = config
        self.spark = spark
        self.logger = FrameworkLogger.get_logger("BronzePipeline")

    def execute(self):

        self.logger.info(
            f"Executing Bronze Pipeline : {self.config.dataset.name}"
        )

        ingestor = DatabricksBronzeIngestor(
            spark=self.spark,
            config=self.config
        )

        ingestor.run()