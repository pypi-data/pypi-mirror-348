import pytest
from config_loader.loader import YamlConfigLoader
from pathlib import Path

BASE = Path(__file__).parent / "resources"

def test_basic_loading():
    loader = YamlConfigLoader(BASE / "base.yml")
    assert loader.get("app.name") == "test-app"
    assert loader.get("app.debug") is False

def test_nested_key_access():
    loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="dev")
    assert loader.get("database.connection.host") == "localhost"
    assert loader.get("database.connection.port") == 5432

def test_profile_override():
    loader = YamlConfigLoader(BASE / "with_profiles.yml", profile="prod")
    assert loader.get("app.debug") is False
    assert loader.get("database.connection.host") == "prod.db.internal"

def test_missing_key_returns_default():
    loader = YamlConfigLoader(BASE / "base.yml")
    assert loader.get("nonexistent.key", default="fallback") == "fallback"

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        YamlConfigLoader("nonexistent.yml")

def test_invalid_yaml_raises():
    with pytest.raises(Exception):
        YamlConfigLoader(BASE / "invalid.yml")
