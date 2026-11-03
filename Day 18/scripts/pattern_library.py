"""Reusable regex patterns for Day 18 practice."""

import re
from datetime import datetime


PATTERNS = {
    "digits": r"\d+",
    "letters": r"[A-Za-z]+",
    "alphanumeric": r"[A-Za-z0-9]+",
    "whitespace": r"\s+",
    "word_boundary": r"\bdata\b",
    "starts_with_capital": r"^[A-Z]",
    "ends_with_period": r"\.$",
    "repeated_character": r"(.)\1+",
    "email": r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b",
    "phone_india": r"(?:\+91[- ]?)?[6-9]\d{9}\b",
    "url": r"https?://[^\s,]+",
    "date_dd_mm_yyyy": r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
    "date_yyyy_mm_dd": r"\b\d{4}-\d{2}-\d{2}\b",
    "time_24_hour": r"\b(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\b",
    "ip_address_format": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "username": r"\b[A-Za-z][A-Za-z0-9_]{2,19}\b",
    "postal_code_india": r"\b[1-9]\d{5}\b",
    "hex_color": r"#[0-9A-Fa-f]{6}\b",
    "html_tag": r"</?[A-Za-z][A-Za-z0-9]*(?:\s[^<>]*)?>",
    "remove_special_characters": r"[^A-Za-z0-9 ]",
    "multiple_spaces": r" {2,}",
    "log_level": r"\b(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)\b",
    "log_line": (
        r"^(?P<date>\d{4}-\d{2}-\d{2}) "
        r"(?P<time>\d{2}:\d{2}:\d{2}) "
        r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
        r"(?P<message>.*)$"
    ),
    "extract_number": r"[-+]?\d*\.?\d+",
}

# Demonstrate that the patterns can be reused.
if __name__ == "__main__":
    sample = "Contact sales.team@zoe.in or call +91 9876543210."

    for name in ("email", "phone_india"):
        matches = re.findall(PATTERNS[name], sample)
        print(f"{name}: {matches}")

    print(f"Pattern count: {len(PATTERNS)}")