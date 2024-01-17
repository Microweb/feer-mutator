from datetime import date, timedelta

from .entities import Period


def get_period(relative_day: int | None = None) -> Period:
    relative_day = -1 if relative_day is None else relative_day
    today = date.today()
    yesterday = today + timedelta(days=relative_day)
    return Period(yesterday, yesterday)
