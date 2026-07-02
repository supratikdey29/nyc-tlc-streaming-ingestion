from pyspark.sql import SparkSession

from framework.orchestration.pipeline_runner import PipelineRunner

spark = SparkSession.getActiveSession()

runner = PipelineRunner(
    spark=spark
)

runner.run(
    environment=env,
    dataset=dataset
)