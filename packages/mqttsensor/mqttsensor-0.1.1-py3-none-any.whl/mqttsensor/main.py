from mqttsensor.config import Config
from mqttsensor.mqtt.client import MqttClient


def init_client(config_file: str = "config.toml") -> tuple[Config, MqttClient]:
    """
    Main function to initialize the configuration and MQTT client.
    """
    config = Config(config_file)
    mqtt_client = MqttClient(**config.get(["mqtt"]))
    return config, mqtt_client


def main():
    """
    Main entry point for the MQTT sensor application.
    """
    config, mqtt_client = init_client()
    mqtt_client.start()
    mqtt_client.stop()
