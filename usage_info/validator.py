import datetime
import typing as typ


class ValidationError(Exception):
    """Data validation exception"""


def date_validator(date: str) -> str:
    """Check if the date format is correct

    :param date: date in format %Y-%m-%d or None. e.g 2017-06-01
    :return: date
    :raise ValidationError: if the date format is not correct
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        raise ValidationError(f"Got not correct date format: {date!r}")
    return date


def comma_separated_str(allowed: typ.Optional[set] = None):
    """Decorator to specify allowed values

    :param allowed: allowed values (optional)
    :return: inner function
    """
    def inner(raw_str: str) -> str:
        """Check if the comma separated string format is correct

        :param raw_str: comma separated string. e.g. adcolony,vungle
        :return: raw_str
        :raise ValidationError: if the comma separated string format is not correct
        """
        for str_ in raw_str.split(','):
            if not str_ or str_.isdigit():
                raise ValidationError(
                    f'Got not correct comma separated format'
                    f': {raw_str!r} (element {str_!r})')
            if allowed and str_ not in allowed:
                raise ValidationError(
                    f'The {str_!r} field is not allowed. Please choose from {allowed!r}')
        return raw_str
    return inner
