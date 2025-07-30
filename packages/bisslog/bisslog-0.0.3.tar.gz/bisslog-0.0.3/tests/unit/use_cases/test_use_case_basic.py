import pytest
from unittest.mock import MagicMock, patch
import re

from bisslog.exceptions.domain_exception import NotFound, DomainException

from bisslog.use_cases.use_case_basic import BasicUseCase


uuid_regex = re.compile(
    r"[a-fA-F0-9]{8}-"
    r"[a-fA-F0-9]{4}-"
    r"[1-5][a-fA-F0-9]{3}-"
    r"[89abAB][a-fA-F0-9]{3}-"
    r"[a-fA-F0-9]{12}"
)


class SampleUseCase(BasicUseCase):
    """Sample subclass for testing BasicUseCase."""

    def use(self, *args, **kwargs):
        """Mock implementation of the 'use' method."""
        return "use_case_result"


@pytest.fixture
def use_case():
    """Fixture to provide a BasicUseCase instance with mocked dependencies."""
    return SampleUseCase("test_use_case", do_trace=True)


def test_use_case_call(use_case):
    """Ensures calling the use case triggers the 'use' method."""
    result = use_case()
    assert result == "use_case_result"


def test_start_transaction(use_case):
    """Tests if a transaction is correctly started."""
    use_case._transaction_manager.create_transaction_id = MagicMock()
    use_case._transaction_manager.create_transaction_id.return_value = "tx-123"
    use_case._tracing_opener.start = MagicMock()

    transaction_id = use_case._BasicUseCase__start()

    assert transaction_id == "tx-123"
    use_case._tracing_opener.start.assert_called_once()


def test_end_transaction(use_case):
    """Tests if a transaction ends correctly."""
    use_case._transaction_manager.close_transaction = MagicMock()
    use_case._tracing_opener.end = MagicMock()

    use_case._BasicUseCase__end("tx-123", "super-tx-456", "result")

    use_case._transaction_manager.close_transaction.assert_called_once()
    use_case._tracing_opener.end.assert_called_once_with(
        transaction_id="tx-123", component="test_use_case",
        super_transaction_id="super-tx-456", result="result"
    )

@patch.object(SampleUseCase, "use", side_effect=ValueError("test error"))
def test_use_case_exception_handling(mock_use, caplog):
    """Ensures exceptions are logged and re-raised."""
    use_case = SampleUseCase("test_use_case", do_trace=True)

    with caplog.at_level("CRITICAL"):
        with pytest.raises(ValueError, match="test error"):
            use_case.__call__()

    mock_use.assert_called_once()

@patch.object(SampleUseCase, "use", side_effect=NotFound("basic", "domain test error"))
def test_use_case_domain_exception_handling(mock_use, caplog):
    """Ensures domain exception are logged and re-raised."""
    use_case = SampleUseCase("test_use_case", do_trace=True)

    with caplog.at_level("CRITICAL"):
        with pytest.raises(DomainException, match="domain test error"):
            use_case.__call__()

    mock_use.assert_called_once()
