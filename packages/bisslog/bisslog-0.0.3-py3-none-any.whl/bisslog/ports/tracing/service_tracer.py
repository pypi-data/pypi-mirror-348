"""Module defining the ServiceTracer interface."""

from abc import ABC, abstractmethod
from typing import Optional

from .tracer import Tracer


class ServiceTracer(Tracer, ABC):
    """Abstract base class for service tracing.

    This class extends `Tracer` and defines a contract for implementing
    service-level tracing mechanisms.

    Notes
    -----
    - This class is intended to be subclassed by specific service tracing implementations.
    - It does not define any concrete methods but serves as a structural base."""

    @abstractmethod
    def info(self, payload: object, *args, checkpoint_id: Optional[str] = None,
             extra: dict = None, **kwargs):
        """Logs an informational message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional logging context, by default None."""
        raise NotImplementedError("TracingManager must implement method info")

    @abstractmethod
    def debug(self, payload: object, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs a debug message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method debug")

    @abstractmethod
    def warning(self, payload: object, *args, checkpoint_id: Optional[str] = None,
                extra: dict = None, **kwargs):
        """Logs a warning message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method warning")

    @abstractmethod
    def error(self, payload: object, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs an error message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method error")

    @abstractmethod
    def critical(self, payload: object, *args, checkpoint_id: Optional[str] = None,
                 extra: dict = None, **kwargs):
        """Logs a critical error message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method critical")
