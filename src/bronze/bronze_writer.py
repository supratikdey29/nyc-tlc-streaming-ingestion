from framework.logging.logger import FrameworkLogger


class BronzeWriter:

    def __init__(self, config):

        self.config = config

        self.logger = FrameworkLogger.get_logger(
            "BronzeWriter"
        )

    ############################################################

    def write(self, dataframe):

        self.logger.info("Writing Bronze stream...")

        checkpoint_path = self.config.checkpoint.path

        target_table = (
            f"{self.config.target.catalog}."
            f"{self.config.target.schema_name}."
            f"{self.config.target.table}"
        )

        writer = (
            dataframe.writeStream
            .format("delta")
            .outputMode(self.config.streaming.mode)
            .option(
                "checkpointLocation",
                checkpoint_path
            )
            .option(
                "mergeSchema",
                "true"
            )
        )

        if self.config.streaming.trigger == "availableNow":

            writer = writer.trigger(
                availableNow=True
            )

        elif self.config.streaming.trigger == "once":

            writer = writer.trigger(
                once=True
            )

        else:

            writer = writer.trigger(
                processingTime=self.config.streaming.trigger
            )

        self.logger.info(
            "\nBronze Writer\n"
            f"Target Table : {target_table}\n"
            f"Checkpoint   : {checkpoint_path}\n"
            f"Trigger      : {self.config.streaming.trigger}"
        )

        self.logger.info(
            "Starting streaming query..."
        )

        query = writer.table(target_table)

        self.logger.info(
            "Streaming query started successfully."
        )

        return query