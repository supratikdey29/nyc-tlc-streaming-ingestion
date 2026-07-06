from framework.logging.logger import FrameworkLogger

from bronze.databricks_bronze import DatabricksBronzeIngestor
from bronze.bronze_transformer import BronzeTransformer
from bronze.bronze_writer import BronzeWriter


class BronzePipeline:

    def __init__(self, config, spark=None):

        self.config = config
        self.spark = spark

        self.logger = FrameworkLogger.get_logger(
            "BronzePipeline"
        )

    ############################################################

    def execute(self):

        self.logger.info(
            f"Executing Bronze Pipeline : {self.config.dataset.name}"
        )

        ########################################################
        # Read
        ########################################################

        ingestor = DatabricksBronzeIngestor(
            spark=self.spark,
            config=self.config
        )

        dataframe = ingestor.read()

        ########################################################
        # Transform
        ########################################################

        transformer = BronzeTransformer()

        dataframe = transformer.transform(
            dataframe
        )

        ########################################################
        # Write
        ########################################################

        writer = BronzeWriter(
            self.config
        )

        query = writer.write(
            dataframe
        )

        ########################################################
        # Wait for completion
        ########################################################

        self.logger.info(
            "Waiting for stream completion..."
        )

        query.awaitTermination()

        self.logger.info(
            "Bronze Pipeline completed successfully."
        )