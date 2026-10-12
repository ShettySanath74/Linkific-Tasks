
import unittest

from salary_utils import (
    validate_salary,
    calculate_annual_salary,
    normalize_name,
)


class TestSalaryUtils(unittest.TestCase):

    def test_valid_salary(self):
        self.assertTrue(validate_salary(45000))

    def test_negative_salary(self):
        self.assertFalse(validate_salary(-100))

    def test_zero_salary(self):
        self.assertFalse(validate_salary(0))

    def test_non_numeric_salary(self):
        self.assertFalse(validate_salary("abc"))

    def test_annual_salary(self):
        self.assertEqual(
            calculate_annual_salary(45000),
            540000.0
        )

    def test_invalid_annual_salary(self):
        with self.assertRaises(ValueError):
            calculate_annual_salary(-100)

    def test_normalize_name(self):
        self.assertEqual(
            normalize_name("  aSHA   SHETTY "),
            "Asha Shetty"
        )

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            normalize_name("   ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
