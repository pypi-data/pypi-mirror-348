"""Use case tracking system class implementation.

This module provides an abstract base class `BasicUseCase` that integrates
transactional tracing into a use case execution flow."""

from abc import ABC
from typing import Optional

from .use_case_base import UseCaseBase
from ..transactional.transaction_traceable import TransactionTraceable


class BasicUseCase(UseCaseBase, TransactionTraceable, ABC):
    """Abstract base class for use cases with transactional tracing.

    This class provides a structured way to execute use cases while tracking
    transactions using a tracing system."""

    def __init__(self, keyname: Optional[str] = None, *, do_trace: bool = True) -> None:
        """Initializes the use case with optional tracing.

        Parameters
        ----------
        keyname : Optional[str]
            Unique identifier for the use case.
        do_trace : bool, optional
            Determines if tracing should be enabled (default is True)."""
        UseCaseBase.__init__(self, keyname)
        TransactionTraceable.__init__(self)
        self._do_trace = do_trace

    def __call__(self, *args, **kwargs):
        """Makes the use case callable, triggering its execution.

        Parameters
        ----------
        *args
            Positional arguments for the use case.
        **kwargs
            Keyword arguments for the use case.

        Returns
        -------
        object
            The result of the use case execution."""
        return self._use(*args, **kwargs)

    def __start(self, *args, super_transaction_id: Optional[str] = None, **kwargs) -> Optional[str]:
        """Starts a transaction for the use case.

        If tracing is enabled or no parent transaction is provided, a new transaction is created.

        Parameters
        ----------
        *args
            Positional arguments.
        super_transaction_id : Optional[str], optional
            The ID of an existing transaction that this use case is part of.
        **kwargs
            Additional keyword arguments.

        Returns
        -------
        Optional[str]
            The transaction ID created or the provided parent transaction ID."""
        if self._do_trace or super_transaction_id is None:
            transaction_id = self._transaction_manager.create_transaction_id(self.keyname)

            self._tracing_opener.start(*args, super_transaction_id=super_transaction_id,
                                       component=self.keyname,
                                       transaction_id=transaction_id, **kwargs)
            return transaction_id
        return super_transaction_id

    def __end(self, transaction_id: str, super_transaction_id: Optional[str], result: object):
        """Ends the transaction after use case execution.

        If tracing is enabled, it ensures the transaction is properly closed.

        Parameters
        ----------
        transaction_id : str
            The transaction ID of the executed use case.
        super_transaction_id : Optional[str]
            The ID of the parent transaction, if any.
        result : object
            The result of the use case execution."""
        if self._do_trace:
            self._transaction_manager.close_transaction()
            self._tracing_opener.end(transaction_id=transaction_id, component=self.keyname,
                                     super_transaction_id=super_transaction_id, result=result)

    def _use(self, *args, **kwargs):
        """Executes the use case with transactional tracing.

        This method manages the transaction lifecycle before and after executing
        the `use` method, ensuring proper logging and error handling.

        Parameters
        ----------
        *args
            Positional arguments for the use case.
        **kwargs
            Keyword arguments for the use case.

        Returns
        -------
        object
            The result of the use case execution.

        Raises
        ------
        BaseException
            If an error occurs during execution, it is logged and re-raised."""
        super_transaction_id = kwargs.pop("transaction_id", None)
        transaction_id = self.__start(*args, super_transaction_id=super_transaction_id, **kwargs)
        if super_transaction_id is None:
            super_transaction_id = transaction_id

        res = self.use(*args, transaction_id=transaction_id, **kwargs)
        self.__end(transaction_id=transaction_id,
                   super_transaction_id=super_transaction_id, result=res)
        return res
