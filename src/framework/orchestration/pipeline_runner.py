from pathlib import Path
import argparse
import uuid

from framework.logging.logger import FrameworkLogger
from framework.configuration.config_loader import ConfigLoader
from framework.orchestration.pipeline_factory import PipelineFactory


logger = FrameworkLogger.get_logger("PipelineRunner")


class PipelineRunner:
    """
    Central orchestration engine.

    Responsibilities
    ----------------
    1. Load configuration
    2. Create pipeline
    3. Execute pipeline
    """

    ############################################################

    def __init__(self, project_root: Path, spark=None):

        self.project_root = project_root
        self.spark = spark

        self.loader = ConfigLoader(project_root)

        self.config = None
        self.pipeline = None

    ############################################################

    def _log_banner(self):

        logger.info("======================================")
        logger.info("NYC TLC INGESTION FRAMEWORK")
        logger.info("======================================")

    ############################################################

    def load_configuration(self, environment: str, dataset: str):

        logger.info(
            f"Loading configuration\n"
            f"Environment : {environment}\n"
            f"Dataset     : {dataset}"
        )

        self.config = self.loader.load(
            environment,
            dataset
        )

        logger.info("[CONFIGURATION LOADED]")

        logger.info(
            "\nPipeline Configuration\n"
            f"Environment : {environment}\n"
            f"Dataset     : {self.config.dataset.name}\n"
            f"Source      : {self.config.source.path}\n"
            f"Target      : "
            f"{self.config.target.catalog}."
            f"{self.config.target.schema_name}."
            f"{self.config.target.table}"
        )

    ############################################################

    def create_pipeline(self):

        logger.info("Creating pipeline...")

        self.pipeline = PipelineFactory.get_pipeline(
            config=self.config,
            spark=self.spark
        )

        logger.info(
            f"Pipeline created : "
            f"{type(self.pipeline).__name__}"
        )

    ############################################################

    def execute_pipeline(self):

        logger.info("Executing pipeline...")

        self.pipeline.execute()

        logger.info(
            "Pipeline execution completed."
        )

    ############################################################

    def run(self, environment: str, dataset: str):

        FrameworkLogger.set_run_id(
            str(uuid.uuid4())[:8]
        )

        self._log_banner()

        try:

            self.load_configuration(
                environment,
                dataset
            )

            self.create_pipeline()

            self.execute_pipeline()

            logger.info(
                "Framework completed successfully."
            )

        except Exception as ex:

            logger.exception(
                f"Pipeline execution failed: {ex}"
            )

            raise

############################################################


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        required=True
    )

    parser.add_argument(
        "--dataset",
        required=True
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[3]

    runner = PipelineRunner(
        project_root=project_root
    )

    runner.run(
        environment=args.env,
        dataset=args.dataset
    )


if __name__ == "__main__":
    main()