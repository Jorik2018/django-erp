from django.db.models import Q, Sum
from django.utils import timezone

from expense.models import Expense


def expense_totals(request):
    """
    Return total expenses, current month expenses,
    and current year expenses.
    """

    current = timezone.localdate()

    totals = Expense.objects.aggregate(
        total_expense=Sum("amount"),

        total_expense_by_month=Sum(
            "amount",
            filter=Q(
                date__year=current.year,
                date__month=current.month,
            ),
        ),

        total_expense_by_year=Sum(
            "amount",
            filter=Q(
                date__year=current.year,
            ),
        ),
    )

    return {
        "total_expense": totals["total_expense"] or 0,
        "total_expense_by_month": totals["total_expense_by_month"] or 0,
        "total_expense_by_year": totals["total_expense_by_year"] or 0,
    }