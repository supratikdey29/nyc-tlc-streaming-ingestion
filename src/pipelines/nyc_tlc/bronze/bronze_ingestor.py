import pandas as pd
from pathlib import Path
import json
from datetime import datetime


class BronzeIngestor:
    """
    Simulates Bronze ingestion layer (Databricks-style).
    """

    def __init__(self, target_path: str, checkpoint_file: str):
        self.target_path = Path(target_path)
        self.checkpoint_file = Path(checkpoint_file)

        self.processed_files = self._load_checkpoint()

    def _load_checkpoint(self):
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, "r") as f:
                return set(json.load(f))
        return set()

    def _save_checkpoint(self):
        with open(self.checkpoint_file, "w") as f:
            json.dump(list(self.processed_files), f)

    def ingest(self, files: list):
        """
        Process new files into Bronze layer.
        """

        all_dfs = []

        for file in files:
            print(f"[BRONZE] Processing {file}")

            df = pd.read_parquet(file)

            # Add metadata columns (enterprise pattern)
            df["ingestion_timestamp"] = datetime.utcnow().isoformat()
            df["source_file"] = file

            all_dfs.append(df)

            self.processed_files.add(file)

        if all_dfs:
            final_df = pd.concat(all_dfs)

            self._write_bronze(final_df)

        self._save_checkpoint()

    def _write_bronze(self, df: pd.DataFrame):
        """
        Simulates writing to Delta Bronze layer.
        """

        self.target_path.mkdir(parents=True, exist_ok=True)

        output_file = self.target_path / "bronze_data.parquet"

        df.to_parquet(output_file, index=False)

        print(f"[BRONZE] Written to {output_file}")