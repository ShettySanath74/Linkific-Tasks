"""Shared paths and logging for Day 27."""
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "data" / "source"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DEAD_LETTER_DIR = PROJECT_ROOT / "data" / "dead_letter"
LOG_DIR = PROJECT_ROOT / "logs"
EXTRACT_DIR = OUTPUT_DIR / "extracted"
TRANSFORM_DIR = OUTPUT_DIR / "transformed"
DATABASE_PATH = OUTPUT_DIR / "warehouse.db"

def ensure_directories():
    for path in (SOURCE_DIR, OUTPUT_DIR, DEAD_LETTER_DIR, LOG_DIR, EXTRACT_DIR, TRANSFORM_DIR):
        path.mkdir(parents=True, exist_ok=True)

def get_logger(name):
    ensure_directories()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        fh = logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8")
        sh = logging.StreamHandler()
        fh.setFormatter(fmt); sh.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(sh)
    return logger
