from framework.logging.logger import FrameworkLogger
from stream.autoloader_reader import AutoLoaderReader


class DatabricksBronzeIngestor:

    def __init__(self, spark, config):

        self.spark = spark
        self.config = config

        self.logger = FrameworkLogger.get_logger(
            "DatabricksBronzeIngestor"
        )

    ############################################################

    def read(self):

        self.logger.info(
            "Bronze Reader Started"
        )

        self._log_configuration()

        reader = AutoLoaderReader(
            spark=self.spark,
            config=self.config
        )

        return reader.read()

    ############################################################

    def _log_configuration(self):

        self.logger.info(
            "\nBronze Configuration\n"
            f"Source      : {self.config.source.path}\n"
            f"Catalog     : {self.config.target.catalog}\n"
            f"Schema      : {self.config.target.schema_name}\n"
            f"Table       : {self.config.target.table}\n"
            f"Checkpoint  : {self.config.checkpoint.path}\n"
            f"Trigger     : {self.config.streaming.trigger}"
        )