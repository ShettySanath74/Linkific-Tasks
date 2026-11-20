"""Shared paths and logging helpers for the Day 26 ETL pipeline."""
from __future__ import annotations

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


def ensure_directories() -> None:
    """Create runtime directories if they do not already exist."""
    for directory in (
        OUTPUT_DIR, DEAD_LETTER_DIR, LOG_DIR, EXTRACT_DIR, TRANSFORM_DIR
    ):
        directory.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a console + file logger without adding duplicate handlers."""
    ensure_directories()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler = logging.FileHandler(
            LOG_DIR / "pipeline.log", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
