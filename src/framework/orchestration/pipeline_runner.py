from pathlib import Path
import argparse

import uuid
from framework.logging.logger import FrameworkLogger

#from framework.logging.logger import FrameworkLogger
from framework.configuration.config_loader import ConfigLoader
from framework.orchestration.pipeline_factory import PipelineFactory

logger = FrameworkLogger.get_logger("PipelineRunner")


class PipelineRunner:
    """
    Central orchestration engine.

    Responsibilities:
        1. Load metadata
        2. Build pipeline
        3. Execute pipeline
    """

    def __init__(self, project_root: Path):

        self.project_root = project_root

        self.loader = ConfigLoader(project_root)

        self.config = None

        self.pipeline = None

    ############################################################

    def load_configuration(self, environment: str, dataset: str):

        logger.info(
            f"Loading configuration\n"
            f"Environment : {environment}\n"
            f"Dataset     : {dataset}"
        )

        self.config = self.loader.load(environment, dataset)

        logger.info("[CONFIGURATION LOADED]")

        #logger.info(self.config)
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

        self.pipeline = PipelineFactory.get_pipeline(self.config)

        logger.info(
            f"Pipeline created : {type(self.pipeline).__name__}"
        )

    ############################################################

    def execute_pipeline(self):

        logger.info("Executing pipeline...")

        #pipeline = PipelineFactory.get_pipeline(config)

        self.pipeline.execute()

        logger.info("Pipeline execution completed.")

    ############################################################

    def run(self, environment: str, dataset: str):

        run_id = str(uuid.uuid4())[:8]
        FrameworkLogger.set_run_id(run_id)

        logger.info("======================================")

        logger.info("NYC TLC INGESTION FRAMEWORK")

        logger.info("======================================")
        
        try:

            self.load_configuration(environment, dataset)

            self.create_pipeline()

            self.execute_pipeline()

            logger.info("Framework completed successfully.")
        
        except Exception as ex:

            logger.exception(
                f"Pipeline execution failed: {str(ex)}"
            )

            raise

############################################################


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--env", required=True)

    parser.add_argument("--dataset", required=True)

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[3]

    runner = PipelineRunner(project_root)

    runner.run(args.env, args.dataset)


if __name__ == "__main__":
    main()