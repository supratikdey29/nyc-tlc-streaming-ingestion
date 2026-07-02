from pipelines.nyc_tlc.bronze.bronze_pipeline import BronzePipeline


class PipelineFactory:
    """
    Responsible for returning the correct pipeline implementation
    based on metadata.
    """

    @staticmethod
    def get_pipeline(config, spark=None):

        # Bronze
        if config.target.schema_name.endswith("_bronze"):
            return BronzePipeline(config, spark)

        # Later...
        # if config.target.schema_name.endswith("_silver"):
        #     return SilverPipeline(config, spark)

        raise ValueError(
            f"No pipeline registered for schema {config.target.schema_name}"
        )