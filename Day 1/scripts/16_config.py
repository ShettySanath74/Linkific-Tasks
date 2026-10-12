
from pathlib import Path

# Find the root of the project
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Project folders
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
LOG_DIR = OUTPUT_DIR / "logs"

# Application settings
APP_NAME = "Python Data Engineering Pipeline"
LOG_LEVEL = "INFO"

# Create output folders if they do not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

