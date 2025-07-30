import pytest
import tempfile
import os
from mqttsensor.config import Config


@pytest.fixture
def valid_toml_file():
    fd, path = tempfile.mkstemp(suffix=".toml")
    with os.fdopen(fd, "w") as f:
        f.write(
            "[mqtt]\n"
            'broker="localhost"\n'
            "port=1883\n"
            'client_id="test"\n'
            'ca_certs="ca.pem"\n'
            'certfile="cert.pem"\n'
            'key="key.pem"\n'
            "max_times=3\n"
        )
        f.write('[section]\nkey="value"\n')
    yield path
    os.remove(path)


@pytest.fixture
def invalid_toml_file_missing_mqtt():
    fd, path = tempfile.mkstemp(suffix=".toml")
    with os.fdopen(fd, "w") as f:
        f.write('[section]\nkey="value"\n')
    yield path
    os.remove(path)


@pytest.fixture
def invalid_toml_file_missing_mqtt_key():
    fd, path = tempfile.mkstemp(suffix=".toml")
    with os.fdopen(fd, "w") as f:
        f.write(
            "[mqtt]\n"
            'broker="localhost"\n'
            "port=1883\n"
            'client_id="test"\n'
            'ca_certs="ca.pem"\n'
            'certfile="cert.pem"\n'
            # missing 'key' and 'max_times'
        )
    yield path
    os.remove(path)


def test_read_config(valid_toml_file):
    cfg = Config(valid_toml_file)
    assert "section" in cfg.settings
    assert cfg.settings["section"]["key"] == "value"


def test_get_existing_key(valid_toml_file):
    cfg = Config(valid_toml_file)
    assert cfg.get("section") == {"key": "value"}


def test_get_missing_key(valid_toml_file):
    cfg = Config(valid_toml_file)
    assert cfg.get("missing") is None


def test_wrong_extension():
    with pytest.raises(ValueError):
        Config("not_a_toml.txt")


def test_invalid_config_missing_mqtt(invalid_toml_file_missing_mqtt):
    with pytest.raises(ValueError):
        Config(invalid_toml_file_missing_mqtt)


def test_invalid_config_missing_mqtt_key(invalid_toml_file_missing_mqtt_key):
    with pytest.raises(ValueError):
        Config(invalid_toml_file_missing_mqtt_key)
