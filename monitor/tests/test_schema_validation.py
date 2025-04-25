import pytest

from pykwalify.errors import SchemaError
from pykwalify.core import Core

def test_valid_config():
    """Test that a valid configuration passes schema validation"""
    valid_config = [
        {
            "name": "Test Endpoint",
            "url": "https://example.com",
            "method": "GET"
        }
    ]
    
    core = Core(source_data=valid_config, schema_files=["config-schema.yaml"])
    core.validate()  # Should not raise any exceptions

def test_invalid_config_missing_required():
    """Test that a config missing required fields fails validation"""
    invalid_config = [
        {
            "url": "https://example.com"  # Missing required 'name' field
        }
    ]
    
    core = Core(source_data=invalid_config, schema_files=["config-schema.yaml"])
    with pytest.raises(SchemaError):
        core.validate()

def test_invalid_config_invalid_method():
    """Test that an invalid HTTP method fails validation"""
    invalid_config = [
        {
            "name": "Test Endpoint",
            "url": "https://example.com",
            "method": "INVALID_METHOD"  # Invalid HTTP method
        }
    ]
    
    core = Core(source_data=invalid_config, schema_files=["config-schema.yaml"])
    with pytest.raises(SchemaError):
        core.validate()

def test_invalid_config_invalid_url():
    """Test that an invalid URL format fails validation"""
    invalid_config = [
        {
            "name": "Test Endpoint",
            "url": "not-a-url"  # Invalid URL format
        }
    ]
    
    core = Core(source_data=invalid_config, schema_files=["config-schema.yaml"])
    with pytest.raises(SchemaError):
        core.validate()

def test_valid_config_with_optional_fields():
    """Test that a config with all optional fields passes validation"""
    valid_config = [
        {
            "name": "Test Endpoint",
            "url": "https://example.com",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "body": "{}"
        }
    ]
    
    core = Core(source_data=valid_config, schema_files=["config-schema.yaml"])
    core.validate()  # Should not raise any exceptions

def test_invalid_config_extra_fields():
    """Test that a config with extra fields fails validation"""
    invalid_config = [
        {
            "name": "Test Endpoint",
            "url": "https://example.com",
            "extra_field": "should not be allowed"  # Extra field not in schema
        }
    ]
    
    core = Core(source_data=invalid_config, schema_files=["config-schema.yaml"])
    with pytest.raises(SchemaError):
        core.validate() 