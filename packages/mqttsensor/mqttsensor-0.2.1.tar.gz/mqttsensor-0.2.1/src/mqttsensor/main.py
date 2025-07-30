from mqttsensor.config import Config
from mqttsensor.mqtt.client import MqttClient
from loguru import logger

from mqttsensor import __version__ as version


def init_client(config_file: str = "config.toml") -> tuple[Config, MqttClient]:
    """
    Main function to initialize the configuration and MQTT client.
    """
    config = Config(config_file)
    mqtt_client = MqttClient(**config.get("mqtt"))
    return config, mqtt_client


def main():
    logger.info("Downloaded module correctly")
    logger.info(f"Version: {version}")
