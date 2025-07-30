import pytest

from bisslog.adapt_handler.adapt_handler import AdaptHandler
from bisslog.adapters.blank_adapter import BlankAdapter
from bisslog.domain_context import domain_context


@pytest.fixture
def mock_service_tracer():
    """Mock traceability service."""

    class MockServiceTracer:
        def __init__(self):
            self.warnings = []

        def warning(self, message, checkpoint_id=None):
            self.warnings.append((message, checkpoint_id))

    return MockServiceTracer()


@pytest.fixture
def mock_domain_context(mock_service_tracer):
    """Mock for context domain"""
    domain_context.service_tracer = mock_service_tracer
    return domain_context


@pytest.fixture
def adapt_handler(mock_domain_context):
    """AdaptHandler instance with mocks"""
    return AdaptHandler(component="test_component")


def test_initialization(adapt_handler):
    """test if the initialization is correct"""
    assert adapt_handler.component == "test_component"
    assert adapt_handler._divisions == {}


def test_register_main_adapter(adapt_handler):
    """test that main registration is valid"""
    mock_adapter = object()
    adapt_handler.register_main_adapter(mock_adapter)
    assert adapt_handler._divisions["main"] == mock_adapter


def test_register_adapters(adapt_handler):
    """Verifica que los adaptadores se registren correctamente."""
    adapter1 = object()
    adapter2 = object()

    adapt_handler.register_adapters(finance=adapter1, sales=adapter2)

    assert adapt_handler._divisions["finance"] == adapter1
    assert adapt_handler._divisions["sales"] == adapter2


def test_register_duplicate_adapter(adapt_handler, mock_service_tracer):
    """Prueba que se detecten divisiones duplicadas y se emita un warning."""
    adapter1 = object()
    adapter2 = object()

    adapt_handler.register_adapters(finance=adapter1)
    adapt_handler.register_adapters(finance=adapter2)

    assert adapt_handler._divisions["finance"] == adapter1
    assert len(mock_service_tracer.warnings) == 1
    assert "The division named 'finance' already exists" in mock_service_tracer.warnings[0][0]
    assert mock_service_tracer.warnings[0][1] == "repeated-division"


def test_generate_blank_adapter(adapt_handler):
    """Tests if a BlankAdapter is generated correctly when a division does not exist."""
    blank_adapter = adapt_handler.generate_blank_adapter("new_division")
    assert isinstance(blank_adapter, BlankAdapter)
    assert blank_adapter.division_name == "new_division"
    assert blank_adapter.original_comp == "test_component"


def test_get_existing_division(adapt_handler):
    """Tests retrieving an existing division returns the correct adapter."""
    adapter = object()
    adapt_handler.register_adapters(finance=adapter)

    result = adapt_handler.get_division("finance")
    assert result == adapter


def test_get_non_existing_division(adapt_handler):
    """Tests if an AttributeError is raised when trying to access a non-existing division."""
    with pytest.raises(AttributeError, match="Division named 'marketing' does not exist."):
        adapt_handler.get_division("marketing")


def test_getattribute_existing_division(adapt_handler):
    """Tests __getattribute__ returns a registered adapter when accessed as an attribute."""
    adapter = object()
    adapt_handler.register_adapters(it=adapter)

    assert adapt_handler.it == adapter


def test_getattribute_creates_blank_adapter(adapt_handler):
    """Tests if __getattribute__ creates and stores a BlankAdapter when a division does not exist."""
    blank_adapter = adapt_handler.unknown_division
    assert isinstance(blank_adapter, BlankAdapter)
    assert blank_adapter.division_name == "unknown_division"
    assert blank_adapter.original_comp == "test_component"
    assert adapt_handler._divisions["unknown_division"] == blank_adapter
