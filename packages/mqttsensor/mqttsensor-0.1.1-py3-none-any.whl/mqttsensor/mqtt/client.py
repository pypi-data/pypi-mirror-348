import paho.mqtt.client as mqtt
from loguru import logger
import ssl
import time
from datetime import datetime, timezone
from mqttsensor.mqtt.message_store import MessageStore

import os
import json


def on_connect_handler(client, userdata, flags, rc, properties):
    logger.debug("Connected with result code " + str(rc))
    client.resend_messages()


def on_disconnect_handler(client, userdata, flags, rc, properties):
    logger.warning("Disconnected with result code " + str(rc))
    if rc != 0:
        logger.info("Unexpected disconnection. Attempting to reconnect...")
        time.sleep(5)
        client.reconnect_loop()


def on_publish_handler(client, userdata, mid, rc, properties):
    logger.debug(f"Message {mid} published.")


class MqttClient(mqtt.Client):
    def __init__(self, broker, port, client_id, ca_certs, certfile, key, max_times=60):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.message_store = MessageStore()
        self.last_will = None
        self.times = 0
        self.max_times = max_times
        self.keepalive = 240

        self.tls_set(
            ca_certs=ca_certs,
            certfile=certfile,
            keyfile=key,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS,
        )

        self.on_connect = on_connect_handler
        self.on_disconnect = on_disconnect_handler
        self.on_publish = on_publish_handler

    def start(self):
        self.loop_start()
        self.connect(self.broker, self.port, clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY)

    def stop(self):
        self.loop_stop()

    def send_sensor_data(
        self,
        measurement: str,
        location: str,
        sensor_id: str,
        unit: str,
        value: float | int,
        timestamp: datetime = None,
    ):
        if not timestamp:
            timestamp = datetime.now(timezone.utc)
            logger.warning("Timestamp not provided. Using current UTC time.")

        if not timestamp.tzinfo:
            logger.warning("Timestamp is naive. Setting to UTC.")
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        payload = {
            "unit": unit,
            "value": value,
            "time": timestamp.replace(microsecond=0).isoformat(),
        }
        topic = f"sensors/{measurement}/{location}/{sensor_id}"
        self.publish_messages(topic, json.dumps(payload))

    def publish_messages(self, topic, payload, timeout=1.5):
        message_info = self.publish(topic, payload, qos=1)
        if message_info.rc == mqtt.MQTT_ERR_NO_CONN:
            logger.error("Not connected. Storing message for later.")
            self.message_store.add_message(topic, payload)
        else:
            message_info.wait_for_publish(timeout)

    def resend_messages(self):
        message = self.message_store.get_message()
        while message:
            topic, payload = message
            logger.info(f"Resending message to topic {topic}")
            self.publish_messages(topic, payload, 0.05)
            message = self.message_store.get_message()

    def reconnect_loop(self):
        while self.times < self.max_times:
            try:
                logger.info(f"Attempting to reconnect, times: {self.times}")
                self.start()
                self.times = 0
                break
            except Exception as e:
                logger.error(f"Reconnect failed: {e}")
                self.times += 1
                time.sleep(5)  # Wait before retrying to reconnect
        if self.times >= self.max_times:
            logger.error("Failed to reconnect after multiple attempts.")
            self.stop()
            self.loop_stop()
            raise os._exit(1)
