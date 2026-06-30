import calendar
from datetime import date, timedelta


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


def weekday_occurrences(start: date, end: date, weekday: int) -> list[date]:
    if start > end:
        return []
    days_ahead = (weekday - start.weekday()) % 7
    occurrences = []
    current = start + timedelta(days=days_ahead)
    while current <= end:
        occurrences.append(current)
        current += timedelta(days=7)
    return occurrences


def monthly_occurrences(start: date, end: date, billing_day: int) -> list[date]:
    if start > end:
        return []
    occurrences = []
    year, month = start.year, start.month
    while date(year, month, 1) <= end:
        candidate = next_billing_date(date(year, month, 1), billing_day)
        if start <= candidate <= end:
            occurrences.append(candidate)
        month += 1
        if month > 12:
            month = 1
            year += 1
    return occurrences
