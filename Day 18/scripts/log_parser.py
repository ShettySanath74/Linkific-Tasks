import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "application.log"
OUTPUT_FILE = BASE_DIR / "outputs" / "parsed_logs.csv"

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d) "
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
    r"(?P<message>.*)$"
)


def parse_log_line(line):
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    return match.groupdict()


def main():
    parsed_rows = []
    skipped_lines = 0

    with INPUT_FILE.open("r", encoding="utf-8") as log_file:
        for line in log_file:
            parsed = parse_log_line(line)

            if parsed:
                parsed_rows.append(parsed)
            else:
                skipped_lines += 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["date", "time", "level", "message"]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_rows)

    print(f"Parsed log entries: {len(parsed_rows)}")
    print(f"Skipped malformed lines: {skipped_lines}")
    print(f"Parsed logs saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()