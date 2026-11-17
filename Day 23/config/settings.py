from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

TIMEOUT = int(os.getenv("API_TIMEOUT_SECONDS", "20"))
MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
BACKOFF_SECONDS = float(os.getenv("API_BACKOFF_SECONDS", "2"))
PAGE_SIZE = int(os.getenv("API_PAGE_SIZE", "10"))
BATCH_SIZE = int(os.getenv("FILE_BATCH_SIZE", "100"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()

DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
SOURCE_DB = DATA_DIR / "source_database" / "source.db"
STAGING_DIR = PROJECT_ROOT / "staging"
STATE_FILE = PROJECT_ROOT / "state" / "extraction_state.json"
LOG_DIR = PROJECT_ROOT / "logs"
