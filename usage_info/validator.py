import datetime
import typing as typ


class ValidationError(Exception):
    """Data validation exception"""


def date_validator(date: typ.Optional[str]) -> typ.Optional[str]:
    """Check if the date format is correct

    :param date: date in format %Y-%m-%d or None. e.g 2017-06-01
    :return: date
    :raise ValidationError: if the date format is not correct
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d") if date else None
    except (ValueError, TypeError):
        raise ValidationError(f"Got not correct date format: {date!r}")
    return date
