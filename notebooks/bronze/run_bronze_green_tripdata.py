# ==========================================================
# NYC TLC Bronze Streaming Pipeline
#
# Environment : dev
# Dataset     : green_tripdata
#
# Databricks Job Entry Point
# ==========================================================

import sys
from pathlib import Path

project_root = Path.cwd().parents[1]

sys.path.append(str(project_root / "src"))


from framework.orchestration.pipeline_runner import PipelineRunner


# Repository root
project_root = Path(
    "/Workspace/Repos/supratik.dey29@gmail.com/nyc-tlc-streaming-ingestion"
)

runner = PipelineRunner(
    project_root=project_root,
    spark=spark          # Existing Databricks SparkSession
)

runner.run(
    environment="dev",
    dataset="green_tripdata"
)