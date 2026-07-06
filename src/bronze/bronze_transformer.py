from pyspark.sql.functions import (
    current_timestamp,
    current_date,
    input_file_name,
    lit,
)

from framework.logging.logger import FrameworkLogger


class BronzeTransformer:
    """
    Applies Bronze layer transformations.

    Current Responsibilities
    ------------------------
    - Add ingestion_timestamp
    - Add ingestion_date
    - Add source_file
    - Add run_id

    Future Responsibilities
    -----------------------
    - Standardize column names
    - Normalize null values
    - Metadata enrichment
    - Data cleansing
    """

    def __init__(self):

        self.logger = FrameworkLogger.get_logger(
            "BronzeTransformer"
        )

    ############################################################

    def transform(self, dataframe):

        self.logger.info(
            "Applying Bronze transformations..."
        )

        return (

            dataframe

            .withColumn(
                "ingestion_timestamp",
                current_timestamp()
            )

            .withColumn(
                "ingestion_date",
                current_date()
            )

            .withColumn(
                "source_file",
                input_file_name()
            )

            .withColumn(
                "run_id",
                lit(
                    FrameworkLogger.get_run_id()
                )
            )

        )