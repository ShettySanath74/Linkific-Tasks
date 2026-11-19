import logging
import os
import smtplib
import time
from email.message import EmailMessage
from functools import wraps
from .config import LOG_DIR

def configure_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("day25")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        file_handler = logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger

def retry(attempts=3, delay_seconds=1):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, attempts + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    logging.getLogger("day25").warning(
                        "%s failed (attempt %s/%s): %s",
                        function.__name__, attempt, attempts, exc
                    )
                    if attempt < attempts:
                        time.sleep(delay_seconds * attempt)
            raise last_error
        return wrapper
    return decorator

def send_email_alert(subject, body):
    required = ["SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "ALERT_TO", "ALERT_FROM"]
    if not all(os.getenv(key) for key in required):
        logging.getLogger("day25").warning("Email alert skipped: SMTP environment variables are not fully configured.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.environ["ALERT_FROM"]
    message["To"] = os.environ["ALERT_TO"]
    message.set_content(body)

    port = int(os.getenv("SMTP_PORT", "587"))
    with smtplib.SMTP(os.environ["SMTP_HOST"], port, timeout=20) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(message)
    return True
