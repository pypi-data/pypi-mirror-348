"""Module defining the FullUseCase class."""

from abc import ABC
from typing import Optional

from ..adapt_handler.file_uploader_handler import bisslog_upload_file
from ..adapt_handler.publisher_handler import bisslog_pubsub
from .use_case_basic import BasicUseCase


class FullUseCase(BasicUseCase, ABC):
    """Extends `BasicUseCase` with additional functionalities.

    This class integrates message publishing and file uploading capabilities,
    leveraging predefined adapters."""

    __publisher = bisslog_pubsub.main
    __upload_file_adapter = bisslog_upload_file.main

    def publish(self, queue_name: str, body: object, *args,
                partition: Optional[str] = None, **kwargs) -> None:
        """Publishes a message to the specified queue.

        Parameters
        ----------
        queue_name : str
            The name of the queue where the message should be published.
        body : object
            The message payload to be published.
        *args: tuple
            Arguments to the publisher.
        partition : Optional[str]
            Optional partition identifier for the message.
        **kwargs : dict
            Keyword arguments"""
        self.__publisher(queue_name, body, *args, partition=partition, **kwargs)

    def upload_file_stream(self, remote_path: str, stream: bytes, *args,
                           transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from a byte stream to a remote location.

        Parameters
        ----------
        remote_path : str
            The destination path where the file should be uploaded.
        stream : bytes
            The file content in bytes.
        *args: tuple
            Arguments to file uploader.
        transaction_id : Optional[str], default=None
            Optional transaction identifier.
        **kwargs : dict
            Keyword arguments

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        return self.__upload_file_adapter.upload_file_stream(
            remote_path, stream, *args, transaction_id=transaction_id, **kwargs)

    def upload_file_from_local(self, local_path: str, remote_path: str, *args,
                               transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from a local path to a remote location.

        Parameters
        ----------
        local_path : str
            The local file path to be uploaded.
        remote_path : str
            The destination path where the file should be stored.
        *args: tuple
            Arguments to file uploader.
        transaction_id : Optional[str], default=None
            Optional transaction identifier.
        **kwargs : dict
            Keyword arguments

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        return self.__upload_file_adapter.upload_file_from_local(
            local_path, remote_path, *args, transaction_id=transaction_id, **kwargs)
