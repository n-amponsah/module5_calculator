import logging
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
import pandas as pd

from app.calculation import Calculation
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.operations import Addition


@pytest.fixture
def calculator(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    return Calculator(config=config)


def test_str_method():
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert str(calc) == "Addition(2, 3) = 5"


def test_setup_directories(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = object.__new__(Calculator)
    calc.config = config
    calc._setup_directories()
    assert config.history_dir.exists()


def test_init_load_history_failure_is_warned(tmp_path):
    """Lines 77-79: load_history fails during init, warning is logged."""
    config = CalculatorConfig(base_dir=tmp_path)
    with patch("app.calculator.Calculator.load_history", side_effect=Exception("fail")):
        calc = Calculator(config=config)
    assert calc.history == []


def test_perform_operation_validation_error(calculator):
    """Lines 230-233: ValidationError logged and re-raised."""
    calculator.set_operation(Addition())
    with pytest.raises(ValidationError):
        calculator.perform_operation("abc", 1)


def test_perform_operation_general_exception(calculator):
    """Lines 232-233: general Exception becomes OperationError."""
    calculator.set_operation(Addition())
    with patch("app.calculator.InputValidator.validate_number", side_effect=RuntimeError("boom")):
        with pytest.raises(OperationError):
            calculator.perform_operation(1, 2)


def test_save_history_failure(calculator):
    """Lines 272-275: save_history raises OperationError on failure."""
    calculator.set_operation(Addition())
    calculator.perform_operation(1, 2)
    with patch("pandas.DataFrame.to_csv", side_effect=Exception("disk full")):
        with pytest.raises(OperationError):
            calculator.save_history()


def test_load_history_failure(calculator):
    """Lines 309-312: load_history raises OperationError on failure."""
    pd.DataFrame(
        columns=["operation", "operand1", "operand2", "result", "timestamp"]
    ).to_csv(calculator.config.history_file, index=False)
    with patch("pandas.read_csv", side_effect=Exception("corrupt")):
        with pytest.raises(OperationError):
            calculator.load_history()


def test_undo_empty_returns_false(calculator):
    """Line 371: undo returns False when stack is empty."""
    assert calculator.undo() is False


def test_clear_history(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(1, 2)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []


def test_get_history_dataframe(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(2, 3)
    df = calculator.get_history_dataframe()
    assert len(df) == 1
    assert df.iloc[0]["result"] == "5"


def test_show_history(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(4, 5)
    history = calculator.show_history()
    assert "9" in history[0]


def test_redo(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(1, 2)
    calculator.undo()
    assert calculator.redo() is True


def test_redo_empty(calculator):
    assert calculator.redo() is False


def test_history_trimmed(calculator):
    calculator.config.max_history_size = 2
    calculator.set_operation(Addition())
    calculator.perform_operation(1, 2)
    calculator.perform_operation(3, 4)
    calculator.perform_operation(5, 6)
    assert len(calculator.history) == 2


def test_remove_observer(calculator):
    obs = MagicMock()
    calculator.add_observer(obs)
    calculator.remove_observer(obs)
    assert obs not in calculator.observers


def test_setup_logging_raises(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = object.__new__(Calculator)
    calc.config = config
    with patch("logging.basicConfig", side_effect=OSError("fail")):
        with pytest.raises(OSError):
            calc._setup_logging()

def test_save_history_empty_writes_csv(calculator):
    calculator.history = []
    calculator.save_history()
    df = pd.read_csv(calculator.config.history_file)
    assert df.empty

def test_load_history_empty_df(calculator):
    pd.DataFrame(columns=["operation","operand1","operand2","result","timestamp"]).to_csv(calculator.config.history_file, index=False)
    calculator.history = []
    calculator.load_history()
    assert calculator.history == []
