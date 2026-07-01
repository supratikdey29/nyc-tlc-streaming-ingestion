from pathlib import Path
import yaml

from framework.configuration.config_models import PipelineConfig


class ConfigLoader:
    """
    Loads pipeline configuration from YAML files.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def load(self, environment: str, dataset: str) -> PipelineConfig:
        """
        Load environment + dataset configuration.
        """

        env_file = self.project_root / "configs" / "environments" / f"{environment}.yml"
        dataset_file = self.project_root / "configs" / "ingestion" / f"{dataset}.yml"

        if not env_file.exists():
            raise FileNotFoundError(f"Environment config not found: {env_file}")

        if not dataset_file.exists():
            raise FileNotFoundError(f"Dataset config not found: {dataset_file}")

        with open(env_file, "r") as f:
            env_config = yaml.safe_load(f)

        with open(dataset_file, "r") as f:
            dataset_config = yaml.safe_load(f)

        # Merge configs (dataset overrides env where applicable)
        merged = {**env_config, **dataset_config}

        return PipelineConfig(**merged)