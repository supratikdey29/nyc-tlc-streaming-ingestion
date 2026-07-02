from pathlib import Path
import time
import json


class FileSimulator:
    """
    Simulates streaming file arrival from S3-like directory.
    """

    def __init__(self, source_path: str, state_file: str = "simulation_state.json"):
        #self.source_path = Path(source_path)
        self.source_path = Path(source_path.replace("s3://nyc-tlc-tripdata/Green-Trip-data/", str(Path.home() / "data/nyc-tlc/Green-Trip-data")))
        self.state_file = Path(state_file)

        self.processed_files = self._load_state()

    def _load_state(self):
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                return set(json.load(f))
        return set()

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(list(self.processed_files), f)

    def get_new_files(self):
        all_files = {
            str(f) for f in self.source_path.glob("*.parquet")
        }

        new_files = all_files - self.processed_files
        return list(new_files)

    def mark_processed(self, files):
        for f in files:
            self.processed_files.add(f)
        self._save_state()

    def simulate_stream(self, interval_seconds=10):
        """
        Continuously checks for new files.
        """
        print(f"[SIMULATOR] Watching {self.source_path}")

        while True:
            new_files = self.get_new_files()

            if new_files:
                print(f"[SIMULATOR] New files detected: {len(new_files)}")
                for f in new_files:
                    print(f"  - {f}")

                self.mark_processed(new_files)

            else:
                print("[SIMULATOR] No new files")

            time.sleep(interval_seconds)