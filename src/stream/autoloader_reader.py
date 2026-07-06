from framework.logging.logger import FrameworkLogger


class AutoLoaderReader:
    """
    Encapsulates all Auto Loader read logic.

    Responsibilities
    ----------------
    - Configure Auto Loader
    - Read streaming files
    - Handle schema evolution
    """

    def __init__(self, spark, config):

        self.spark = spark
        self.config = config

        self.logger = FrameworkLogger.get_logger(
            "AutoLoaderReader"
        )

    ############################################################

    def read(self):

        if self.spark is None:
            raise RuntimeError(
                "SparkSession is required."
            )

        reader = self._build_reader()

        dataframe = self._read_stream(reader)

        return dataframe

    ############################################################

    def _build_reader(self):

        self.logger.info(
            "Building Auto Loader reader..."
        )

        reader = (

            self.spark.readStream

                .format("cloudFiles")

                .option(
                    "cloudFiles.format",
                    self.config.source.format
                )

                .option(
                    "pathGlobFilter",
                    self.config.source.file_pattern
                )

                .option(
                    "cloudFiles.schemaLocation",
                    self.config.schema_settings.location
                )

                .option(
                    "cloudFiles.inferColumnTypes",
                    "true"
                )

        )

        mode = self.config.schema_settings.mode

        if mode == "infer":

            reader = reader.option(
                "cloudFiles.schemaEvolutionMode",
                "addNewColumns"
            )

        elif mode == "strict":

            reader = reader.option(
                "cloudFiles.schemaEvolutionMode",
                "none"
            )

        else:

            raise ValueError(
                f"Unsupported schema mode: {mode}"
            )
        return reader

    ############################################################

    def _read_stream(self, reader):

        self.logger.info(
            f"Reading stream from {self.config.source.path}"
        )

        dataframe = reader.load(
            self.config.source.path
        )

        self.logger.info(
            "Streaming DataFrame created successfully."
        )

        #dataframe.printSchema()

        return dataframe