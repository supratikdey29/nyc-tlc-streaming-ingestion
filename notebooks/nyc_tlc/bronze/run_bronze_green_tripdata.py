from pathlib import Path

from framework.orchestration.pipeline_runner import PipelineRunner

project_root = Path("/Workspace/Repos/supratik.dey29@gmail.com/nyc-tlc-streaming-ingestion")

runner = PipelineRunner(project_root)

runner.run(
    environment="dev",
    dataset="green_tripdata"
)