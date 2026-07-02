from projects.nyc_tlc.bronze.bronze_pipeline import BronzePipeline


class PipelineFactory:

    @staticmethod
    def get_pipeline(config):

        dataset = config.dataset.name

        if dataset == "green_tripdata":
            return BronzePipeline(config)

        raise ValueError(
            f"No pipeline found for dataset {dataset}"
        )