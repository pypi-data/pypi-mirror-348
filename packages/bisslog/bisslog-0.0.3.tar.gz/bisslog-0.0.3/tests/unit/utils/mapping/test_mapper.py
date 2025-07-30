import pytest

from bisslog.utils.mapping.mapper import Mapper, ERRORS


def test_mapper_initialization_with_dict():
    base = {"source": "target"}
    mapper = Mapper("test_mapper", base)
    assert mapper.base == base
    assert mapper.name == "test_mapper"
    assert mapper.input_type == "dict"
    assert mapper.output_type == "dict"

def test_mapper_initialization_with_list():
    base = [{"from": "source", "to": "target"}]
    mapper = Mapper("test_mapper", base)
    assert mapper.base == base

def test_mapper_invalid_base_type():
    with pytest.raises(TypeError, match=ERRORS["base-type-error"]):
        Mapper("test_mapper", "invalid_base")

def test_mapper_invalid_base_key():
    base = {123: "target"}  # Invalid key type
    with pytest.raises(TypeError, match=ERRORS["base-kv-type-error"]):
        Mapper("test_mapper", base)

def test_mapper_invalid_base_value():
    base = {"source": 123}  # Invalid value type
    with pytest.raises(TypeError, match=ERRORS["base-kv-type-error"]):
        Mapper("test_mapper", base)

def test_mapper_resource_replacement():
    base = {"$.source": "$.target"}
    resources = {"source": "real_source", "target": "real_target"}
    mapper = Mapper("test_mapper", base, resources=resources)
    assert mapper.base == {"real_source": "real_target"}

def test_mapper_map_dict():
    base = {"user.name": "customer.full_name"}
    mapper = Mapper("test_mapper", base)
    data = {"user": {"name": "John Doe"}}
    result = mapper.map(data)
    assert result == {"customer": {"full_name": "John Doe"}}

def test_mapper_map_list():
    base = [{"from": "user.age", "to": "customer.age"}]
    mapper = Mapper("test_mapper", base)
    data = {"user": {"age": 30}}
    result = mapper.map(data)
    assert result == {"customer": {"age": 30}}

def test_mapper_no_values():
    base = {"": "target"}
    with pytest.raises(ValueError, match=ERRORS["no-values"]):
        Mapper("test_mapper", base)

def test_mapper_no_route():
    base = {"source": ""}
    with pytest.raises(ValueError, match=ERRORS["no-values"]):
        Mapper("test_mapper", base)
