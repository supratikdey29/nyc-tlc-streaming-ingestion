from pathlib import Path
from framework.logging.logger import FrameworkLogger
import argparse

from framework.configuration.config_loader import ConfigLoader


logger = FrameworkLogger.get_logger("PipelineRunner")

#logger.info("Pipeline started")

class PipelineRunner:
    """
    Orchestrates ingestion pipelines in a metadata-driven manner.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.loader = ConfigLoader(project_root)

    def run(self, environment: str, dataset: str):
        """
        Entry point for pipeline execution.
        """

        #logger.info(f"Starting Pipeline execution | environment:{environment} dataset:{dataset}")
        logger.info(
            f"Starting pipeline execution\n"
            f"Environment : {environment}\n"
            f"Dataset     : {dataset}"
        )


        # 1. Load configuration
        config = self.loader.load(environment, dataset)

        logger.info("[CONFIGURATION LOADED]")
        logger.info(config)

        # 2. Placeholder for future stages
        logger.info(
            f"Starting Bronze ingestion\n"
            f"source  : {config.source.path}\n"
            f"Catalog : {config.target.catalog}\n"
            f"Schema  : {config.target.schema_name}\n"
            f"Table   : {config.target.table}\n"
        )
        
        from framework.orchestration.pipeline_factory import PipelineFactory

        pipeline = PipelineFactory.get_pipeline(
            config=config,
            spark=None
        )
        pipeline.execute()

        logger.info("[PIPELINE COMPLETE]")


def main():
    parser = argparse.ArgumentParser(description="NYC TLC Streaming Pipeline")

    parser.add_argument("--env", required=True, help="Environment (dev/qa/prod)")
    parser.add_argument("--dataset", required=True, help="Dataset name")

    args = parser.parse_args()

    #project_root = Path(__file__).resolve().parent.parent
    project_root = Path(__file__).resolve().parents[3]

    runner = PipelineRunner(project_root)

    runner.run(args.env, args.dataset)


if __name__ == "__main__":
    main()