
def validate_salary(salary):
    """Return True if salary is a positive number."""

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        return False

    return salary > 0


def calculate_annual_salary(monthly_salary):
    """Calculate annual salary from monthly salary."""

    if not validate_salary(monthly_salary):
        raise ValueError("Monthly salary must be positive.")

    return float(monthly_salary) * 12


def normalize_name(name):
    """Remove extra spaces and standardize capitalization."""

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string.")

    return " ".join(name.split()).title()
