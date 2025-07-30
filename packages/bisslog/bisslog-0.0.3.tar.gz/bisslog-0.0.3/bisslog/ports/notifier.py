"""Module defining the abstract INotifier class for sending notifications."""

from abc import ABC, abstractmethod


class INotifier(ABC):
    """Abstract base class for a notification sender.

    This interface defines the method required for sending notifications."""

    @abstractmethod
    def __call__(self, notification_obj: object) -> None:
        """Sends a notification.

        Parameters
        ----------
        notification_obj : object
            The notification payload to be sent."""
        raise NotImplementedError("Callable must be implemented")
