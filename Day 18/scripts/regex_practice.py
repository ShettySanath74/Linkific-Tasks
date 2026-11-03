import re
from datetime import datetime

# 1. Email extraction
emails = re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
                    "Contact support@example.com or sales.team@zoe.in")
print("Emails:", emails)

# 2. Phone extraction and cleaning
phones = re.findall(r"(?:\+91[- ]?)?[6-9]\d{9}",
                    "Call +91 9876543210 or 8765432109")
clean_phones = [re.sub(r"\D", "", phone) for phone in phones]
print("Phones:", clean_phones)

# 3. URL extraction
urls = re.findall(r"https?://[^\s,]+",
                  "Visit https://example.com and http://zoe.in")
print("URLs:", urls)

# 4. Date parsing and standardization
date_text = "03-11-2026"
parsed_date = datetime.strptime(date_text, "%d-%m-%Y")
print("Standard date:", parsed_date.strftime("%Y-%m-%d"))

# 5. IP address format check
ip = "192.168.1.10"
ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
print("IP format looks valid:", bool(re.match(ip_pattern, ip)))

# 6. Remove special characters and normalize whitespace
text = "  Customer!!!   data @ clean-up  "
clean_text = re.sub(r"[^A-Za-z0-9 ]", "", text)
clean_text = re.sub(r"\s+", " ", clean_text).strip()
print("Clean text:", clean_text)

# 7. Log parsing
log_line = "2026-11-03 14:25:10 ERROR Failed to connect"
log_pattern = r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.*)$"
match = re.match(log_pattern, log_line)
if match:
    print("Log fields:", match.groupdict())

# 8. re.compile and case-insensitive matching
word_pattern = re.compile(r"data", re.IGNORECASE)
print("Data matches:", word_pattern.findall("Data engineering DATA"))