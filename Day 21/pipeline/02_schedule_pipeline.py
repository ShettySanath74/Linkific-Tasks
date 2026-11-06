
import logging
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]

PIPELINE_SCRIPT = BASE_DIR / "pipeline" / "01_orchestrate_pipeline.py"
LOG_DIR = BASE_DIR / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)


def run_pipeline():
    import subprocess
    import sys

    logging.info("Scheduled pipeline execution started")

    try:
        result = subprocess.run(
            [sys.executable, str(PIPELINE_SCRIPT)],
            check=True,
            capture_output=True,
            text=True
        )

        logging.info("Pipeline output: %s", result.stdout)
        print("Scheduled pipeline executed successfully!")

    except subprocess.CalledProcessError as error:
        logging.error("Pipeline execution failed: %s", error.stderr)
        print("Pipeline execution failed. Check scheduler.log.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Execute once every 24 hours
    scheduler.add_job(
        run_pipeline,
        trigger="interval",
        hours=24,
        next_run_time=datetime.now()
    )

    print("Pipeline scheduler started.")
    print("Pipeline runs immediately and then every 24 hours.")
    print("Press Ctrl+C to stop.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
