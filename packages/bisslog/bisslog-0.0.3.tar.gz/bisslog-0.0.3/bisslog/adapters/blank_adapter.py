"""Module providing a blank adapter implementation."""
from .base_adapter import BaseAdapter


class BlankAdapter(BaseAdapter):
    """Adapter that handles undefined components in a division by logging method calls."""

    def __init__(self, name_division_not_found: str, original_comp: str):
        self.division_name = name_division_not_found
        self.original_comp = original_comp

    def __getattribute__(self, item):
        """Overrides attribute access to provide a blank implementation for undefined methods.

        Parameters
        ----------
        item : str
            The name of the attribute being accessed.

        Returns
        -------
        Callable
            A function that logs the method call with its arguments when invoked."""
        try:
            return super().__getattribute__(item)
        except AttributeError:
            pass

        def blank_use_of_adapter(*args, **kwargs):
            """Logs a message indicating that a method was called on a blank adapter.

            Parameters
            ----------
            *args
                Positional arguments passed to the method.
            **kwargs
                Keyword arguments passed to the method."""
            separator = "#" * 80

            self.log.info(
                "\n" + separator + "\n" +
                f"Blank adapter for {self.original_comp} on division: {self.division_name} \n"
                f"execution of method '{item}' with args {args}, kwargs {kwargs}\n" + separator,
                checkpoint_id="bisslog-blank-division"
            )
        return blank_use_of_adapter
