import logging
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"
LOG_DIR = PROJECT_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_step(script_name):
    script_path = SCRIPTS_DIR / script_name

    print(f"\n{'=' * 55}")
    print(f"Running: {script_name}")
    print("=" * 55)

    logging.info("Starting pipeline step: %s", script_name)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="")

    if result.returncode != 0:
        logging.error("Step failed: %s", script_name)
        raise RuntimeError(f"Pipeline stopped at {script_name}")

    logging.info("Completed pipeline step: %s", script_name)


def main():
    steps = [
    "01_extract_api.py",
    "02_extract_files.py",
    "03_extract_database.py",
    "04_transform_data.py",
    "05_load_warehouse.py",
    "08_validate_warehouse.py",
]

    try:
        for step in steps:
            run_step(step)

        print("\nETL pipeline completed successfully!")
        logging.info("ETL pipeline completed successfully")

    except (RuntimeError, OSError) as error:
        logging.exception("ETL pipeline failed")
        print(f"\nETL pipeline failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()