import toml
from loguru import logger


class Config:
    def __init__(self, config_file: str = "config.toml"):
        if not config_file.endswith(".toml"):
            raise ValueError("Config file must be a .toml file")
        self.config_file = config_file
        self.settings = self.read_config()
        if not self.validate():
            raise ValueError("Invalid configuration file")

    def read_config(self):
        """Read the configuration file and return the settings."""
        with open(self.config_file, "r") as file:
            config = toml.load(file)
        return config

    def get(self, key: str):
        """Get a specific setting from the config."""
        if key in self.settings:
            return self.settings[key]
        else:
            logger.warning(f"Key {key} not found in config.")
            return None

    def validate(self):
        """Validate that the config contains all required MQTT settings."""
        if not self.settings:
            logger.error("Config is empty or invalid.")
            return False

        required_mqtt_keys = [
            "broker",
            "port",
            "client_id",
            "ca_certs",
            "certfile",
            "key",
            "max_times",
        ]

        if "mqtt" not in self.settings:
            logger.error("MQTT configuration missing")
            return False

        mqtt_config = self.settings["mqtt"]
        for key in required_mqtt_keys:
            if key not in mqtt_config:
                logger.error(f"Required MQTT setting '{key}' missing")
                return False

        return True
