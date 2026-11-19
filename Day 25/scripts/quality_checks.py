from datetime import date

def validate_source_headers(actual, required, source_name):
    missing = sorted(required - actual)
    return [] if not missing else [f"{source_name}: missing required columns: {', '.join(missing)}"]

def check_required_fields(record, fields):
    return [f"{field} is null/blank" for field in fields if record.get(field) is None or str(record.get(field)).strip() == ""]

def check_ranges(record):
    errors = []
    try:
        if int(record.get("quantity")) <= 0:
            errors.append("quantity must be greater than zero")
    except (TypeError, ValueError):
        errors.append("quantity must be an integer")
    try:
        if float(record.get("unit_price")) < 0:
            errors.append("unit_price cannot be negative")
    except (TypeError, ValueError):
        errors.append("unit_price must be numeric")
    return errors

def check_date_format(value):
    try:
        date.fromisoformat(str(value))
        return []
    except (TypeError, ValueError):
        return ["order_date must use YYYY-MM-DD"]

def check_duplicates(records, key):
    seen, duplicates = set(), []
    for record in records:
        value = record.get(key)
        if value in seen:
            duplicates.append(value)
        seen.add(value)
    return duplicates

def run_quality_checks(transformed, rejects):
    duplicate_ids = check_duplicates(transformed, "order_id")
    checks = {
        "transformed_records": len(transformed),
        "rejected_records": len(rejects),
        "duplicate_order_ids": duplicate_ids,
        "referential_integrity": "checked during customer/product joins",
        "range_and_type_validation": "checked during transformation",
        "date_format_validation": "checked during transformation",
        "passed": len(rejects) == 0 and not duplicate_ids,
    }
    return checks
