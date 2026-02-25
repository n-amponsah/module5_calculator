import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento

def test_memento_to_dict_returns_history_and_timestamp():
    memento = CalculatorMemento(history=[], timestamp=datetime.datetime.now())

    data = memento.to_dict()

    assert "history" in data
    assert "timestamp" in data
    assert data["history"] == []
    assert isinstance(data["timestamp"], str)
    assert len(data["timestamp"]) > 0


def test_memento_to_dict_serializes_calculations():
    # IMPORTANT: match your project’s Calculation signature:
    # operation is a STRING like "Addition"
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
    )

    memento = CalculatorMemento(history=[calc], timestamp=datetime.datetime.now())
    data = memento.to_dict()

    assert isinstance(data["history"], list)
    assert len(data["history"]) == 1
    assert isinstance(data["history"][0], dict)

    # These keys should exist if Calculation.to_dict() is working
    assert "operation" in data["history"][0]
    assert "operand1" in data["history"][0]
    assert "operand2" in data["history"][0]


def test_memento_from_dict_restores_state():
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("5"),
        operand2=Decimal("2"),
    )

    original = CalculatorMemento(history=[calc], timestamp=datetime.datetime.now())
    data = original.to_dict()

    restored = CalculatorMemento.from_dict(data)

    assert isinstance(restored, CalculatorMemento)
    assert isinstance(restored.history, list)
    assert len(restored.history) == 1
    assert isinstance(restored.history[0], Calculation)
    assert isinstance(restored.timestamp, datetime.datetime)