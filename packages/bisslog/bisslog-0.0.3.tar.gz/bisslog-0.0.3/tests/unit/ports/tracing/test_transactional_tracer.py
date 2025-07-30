import pytest
from unittest.mock import MagicMock
from tests.unit.ports.tracing.fake_transactional_tracer import FakeTransactionalTracer


@pytest.fixture
def transactional_tracer():
    transactional_tracer = FakeTransactionalTracer()
    return transactional_tracer


def test_re_args_with_main(transactional_tracer):
    """Test that _re_args_with_main returns expected dictionary."""
    transactional_tracer._transaction_manager.get_main_transaction_id = MagicMock()
    transactional_tracer._transaction_manager.get_main_transaction_id.return_value = "1234-5678"

    result = transactional_tracer._re_args_with_main()

    assert result == {"transaction_id": "1234-5678", "checkpoint_id": ""}


def test_re_args_with_current(transactional_tracer):
    """Test that _re_args_with_current returns expected dictionary."""
    transactional_tracer._transaction_manager.get_transaction_id = MagicMock()
    transactional_tracer._transaction_manager.get_transaction_id.return_value = "8765-4321"

    result = transactional_tracer._re_args_with_current()

    assert result == {"transaction_id": "8765-4321", "checkpoint_id": ""}
