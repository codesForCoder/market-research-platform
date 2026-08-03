from datetime import datetime


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    # Convert to float first to handle '1.0', '1.0E7', etc.
    return int(float(value))


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None

    value = float(value)

    # Dhan uses -0.01 for non-applicable strike price
    if value == -0.01:
        return None

    return value


def parse_datetime(value: str) -> datetime | None:
    """
    Parses Dhan expiry date.

    Returns None for empty or sentinel values.
    """

    if not value:
        return None

    value = value.strip()

    if value in (
        "",
        "0001-01-01",
        "0001-01-01 00:00:00",
    ):
        return None

    for fmt in (
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    raise ValueError(f"Unsupported datetime format: {value}")


def parse_option_type(value: str | None) -> str | None:
    if value in ("", "XX", None):
        return None

    return value
