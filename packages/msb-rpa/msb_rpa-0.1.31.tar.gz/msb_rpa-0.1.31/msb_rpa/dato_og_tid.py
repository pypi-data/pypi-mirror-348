"""
Module for handling date and time related operations.
"""


def month_conversion(month_name):
    """
    Converts a Danish month name to its corresponding numeric value.

    Args:
        month_name (str): The name of the month in Danish (e.g., 'januar', 'februar').

    Returns:
        int: The numeric value of the month (1-12).

    Raises:
        ValueError: If the month name is not valid.
    """
    months = {
        'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6,
        'juli': 7, 'august': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12
    }

    month_name = month_name.lower().strip()

    if month_name not in months:
        raise ValueError(f"Invalid month name: {month_name}")

    return months[month_name]


def get_last_day_of_month(year, month):
    """
    Finds the last day of a given month for a given year.

    Args:
        year (int): The year (e.g., 2024).
        month (int): The numeric month (1-12).

    Returns:
        int: The last day of the month (28-31).

    Raises:
        ValueError: If the month is out of range (not between 1 and 12).
    """
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")

    num_days_in_month = [31, 29 if _is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    return num_days_in_month[month - 1]


def _is_leap_year(year):
    """
    Determines if a given year is a leap year.

    Args:
        year (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
