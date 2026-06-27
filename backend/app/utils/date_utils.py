import calendar
from datetime import date


def add_months(start: date, months: int) -> date:
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    last_day_of_month = calendar.monthrange(year, month)[1]
    day = min(start.day, last_day_of_month)
    return date(year, month, day)


def next_billing_date(reference: date, billing_day: int) -> date:
    last_day_of_month = calendar.monthrange(reference.year, reference.month)[1]
    day = min(billing_day, last_day_of_month)
    return date(reference.year, reference.month, day)


def month_range(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)
