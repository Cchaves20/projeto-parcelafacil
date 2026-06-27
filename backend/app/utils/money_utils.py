from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(CENTS, rounding=ROUND_HALF_UP)


def split_into_installments(total_amount: Decimal, installments_count: int) -> list[Decimal]:
    base_amount = round_money(total_amount / installments_count)
    amounts = [base_amount] * installments_count
    remainder = round_money(total_amount - base_amount * installments_count)
    amounts[-1] = round_money(amounts[-1] + remainder)
    return amounts
