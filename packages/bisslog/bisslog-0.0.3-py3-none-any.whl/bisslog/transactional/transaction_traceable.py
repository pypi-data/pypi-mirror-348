"""Module implementing transaction traceability support."""

from ..domain_context import domain_context
from ..transactional.transaction_manager import TransactionManager, transaction_manager


class TransactionTraceable:
    """Mixin class providing transaction traceability functionality.

    This class provides properties to access the transaction manager, logging system,
    and tracing opener, facilitating tracking and debugging within a transactional context.

    Properties
    ----------
    log : object
        Provides access to the logging and tracing system from the domain context."""

    @property
    def _transaction_manager(self) -> TransactionManager:
        """Returns the global transaction manager instance."""
        return transaction_manager

    @property
    def log(self):
        """Returns the logging and tracing system from the domain context."""
        return domain_context.tracer

    @property
    def _tracing_opener(self):
        """Returns the tracing opener from the domain context."""
        return domain_context.opener
