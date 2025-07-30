from typing import Optional
from unittest.mock import MagicMock

from bisslog.ports.tracing.transactional_tracer import TransactionalTracer

mock_transaction_manager = MagicMock()

class FakeTransactionalTracer(TransactionalTracer):

    def info(self, payload: object, *args, transaction_id: Optional[str] = None,
             checkpoint_id: Optional[str] = None, **kwargs):
        pass

    def debug(self, payload: object, *args, transaction_id: Optional[str] = None,
              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        pass

    def warning(self, payload: object, *args, transaction_id: Optional[str] = None,
                checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        pass

    def error(self, payload: object, *args, transaction_id: Optional[str] = None,
              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        pass

    def critical(self, payload: object, *args, transaction_id: Optional[str] = None,
                 checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        pass

    def func_error(self, payload, *args, **kwargs):
        pass

    def tech_error(self, payload, *args, **kwargs):
        pass

    def report_start_external(self, payload, *args, **kwargs):
        pass

    def report_end_external(self, payload, *args, **kwargs):
        pass

    def __getattribute__(self, item):
        if item == "_transaction_manager":
            return mock_transaction_manager
        return super().__getattribute__(item)
