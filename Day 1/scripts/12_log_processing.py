
import json
from collections import Counter
from pathlib import Path


# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

LOG_FILE = DATA_DIR / "application.log"
SUMMARY_FILE = OUTPUT_DIR / "log_summary.json"


def analyze_logs(file_path):
    """Read a log file and summarize its contents."""

    log_counts = Counter()
    error_messages = []
    total_lines = 0
    invalid_lines = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            total_lines += 1
            parts = line.split(maxsplit=3)

            # Expected fields: date, time, level, message
            if len(parts) < 4:
                invalid_lines.append({
                    "line_number": line_number,
                    "content": line
                })
                continue

            log_level = parts[2]
            message = parts[3]

            log_counts[log_level] += 1

            if log_level == "ERROR":
                error_messages.append({
                    "line_number": line_number,
                    "message": message
                })

    return {
        "total_lines": total_lines,
        "log_counts": dict(log_counts),
        "error_count": len(error_messages),
        "errors": error_messages,
        "invalid_lines": invalid_lines
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        summary = analyze_logs(LOG_FILE)

    except FileNotFoundError:
        print(f"Log file not found: {LOG_FILE}")
        return

    print("LOG ANALYSIS REPORT")
    print("-" * 30)
    print(f"Total log lines: {summary['total_lines']}")

    print("\nLog level counts:")
    for level, count in sorted(summary["log_counts"].items()):
        print(f"{level}: {count}")

    print(f"\nTotal errors: {summary['error_count']}")

    for error in summary["errors"]:
        print(f"Line {error['line_number']}: {error['message']}")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print(f"\nSummary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
