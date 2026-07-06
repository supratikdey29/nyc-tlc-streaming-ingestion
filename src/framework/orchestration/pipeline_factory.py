from bronze.bronze_pipeline import BronzePipeline


class PipelineFactory:
    """
    Registry of dataset pipelines.

    New datasets can be registered without modifying
    the framework.
    """

    _REGISTRY = {
        "green_tripdata": BronzePipeline,
    }

    ############################################################

    @classmethod
    def register(cls, dataset_name, pipeline_class):

        cls._REGISTRY[dataset_name] = pipeline_class

    ############################################################

    @classmethod
    def get_pipeline(cls, config, spark):

        dataset = config.dataset.name

        pipeline_class = cls._REGISTRY.get(dataset)

        if pipeline_class is None:

            raise ValueError(
                f"No pipeline registered for dataset '{dataset}'"
            )

        return pipeline_class(
            config=config,
            spark=spark
        )