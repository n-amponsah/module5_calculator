from decimal import Decimal
import pytest
from app.calculation import Calculation
from app.exceptions import OperationError


def test_calculate_raises_operation_error_on_arithmetic_failure():
    """Line 81: triggers except block via OverflowError on huge Power operation."""
    with pytest.raises(OperationError, match="Calculation failed"):
        Calculation(
            operation="Power",
            operand1=Decimal("999999999999999999"),
            operand2=Decimal("999999999999999999")
        )


def test_eq_returns_not_implemented_for_non_calculation():
    """Line 222: __eq__ returns NotImplemented when compared to a non-Calculation object."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    result = calc.__eq__("not a calculation")
    assert result is NotImplemented
