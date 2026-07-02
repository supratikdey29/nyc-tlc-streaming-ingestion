from framework.simulation.file_simulator import FileSimulator
from pipelines.nyc_tlc.bronze.bronze_ingestor import BronzeIngestor


SOURCE = "/home/supratik/data/nyc-tlc/Green-Trip-data/"
TARGET = "/home/supratik/data/nyc-tlc/bronze/"
CHECKPOINT = "bronze_checkpoint.json"


sim = FileSimulator(source_path=SOURCE)

ingestor = BronzeIngestor(
    target_path=TARGET,
    checkpoint_file=CHECKPOINT
)

new_files = sim.get_new_files()

print(f"[PIPELINE] New files detected: {len(new_files)}")

if new_files:
    ingestor.ingest(new_files)
    sim.mark_processed(new_files)