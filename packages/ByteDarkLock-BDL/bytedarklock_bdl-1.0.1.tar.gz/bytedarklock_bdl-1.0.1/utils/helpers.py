# utils/helpers.py
"""
Utility helper functions for ByteDarkLock (BDL) module.
This file will contain reusable functions for file operations, logging,
error handling, and other common tasks across the project.

Author: FakeFountain548
"""
import os
import json
import logging
from datetime import datetime, timezone

# Configure basic logger
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%SZ',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def ensure_dir(path: str) -> None:
    """
    Ensure that the directory for a given path exists.
    If the path is a file, ensure its parent directory.
    """
    directory = path if os.path.isdir(path) else os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def read_json(path: str) -> dict:
    """
    Safely read a JSON file and return its contents.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_json(path: str, data: dict, indent: int = 4) -> None:
    """
    Safely write a dictionary to a JSON file, creating directories if needed.
    """
    ensure_dir(path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.debug(f"Wrote JSON to: {path}")


def timestamp_now() -> str:
    """
    Return current UTC timestamp in ISO format.
    """
    return datetime.now(timezone.utc).isoformat()


def log_exception(exc: Exception) -> None:
    """
    Log an exception with traceback.
    """
    logger.error("Exception occurred", exc_info=exc)