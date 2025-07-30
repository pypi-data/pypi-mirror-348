import pytest
from mqttsensor.mqtt.client import MqttClient
from mqttsensor.mqtt.message_store import MessageStore


def test_message_store_add_and_get_message():
    store = MessageStore()
    store.add_message("topic/test", "payload")
    assert len(store) == 1
    msg = store.get_message()
    assert msg == ("topic/test", "payload")
    assert len(store) == 0


def test_message_store_retrieve_messages():
    store = MessageStore()
    store.add_message("topic/1", "a")
    store.add_message("topic/2", "b")
    msgs = store.retrieve_messages()
    assert msgs == [("topic/1", "a"), ("topic/2", "b")]
    assert len(store) == 0


def test_message_store_clear_messages():
    store = MessageStore()
    store.add_message("topic/1", "a")
    store.clear_messages()
    assert len(store) == 0


def test_message_store_has_messages():
    store = MessageStore()
    assert not store.has_messages()
    store.add_message("topic/1", "a")
    assert store.has_messages()


def test_mqttclient_start_calls_connect_and_loop_start(mocker):
    mock_connect = mocker.patch("paho.mqtt.client.Client.connect")
    mock_loop_start = mocker.patch("paho.mqtt.client.Client.loop_start")
    client = MqttClient("broker", 1883, "cid", None, None, None)
    client.start()
    mock_loop_start.assert_called_once()
    mock_connect.assert_called_once()


def test_mqttclient_stop_calls_loop_stop(mocker):
    mock_loop_stop = mocker.patch("paho.mqtt.client.Client.loop_stop")
    client = MqttClient("broker", 1883, "cid", None, None, None)
    client.stop()
    mock_loop_stop.assert_called_once()


def test_mqttclient_publish_messages_stores_on_no_conn(mocker):
    mock_publish = mocker.patch("paho.mqtt.client.Client.publish")
    mock_publish.return_value.rc = 4  # MQTT_ERR_NO_CONN
    client = MqttClient("broker", 1883, "cid", None, None, None)
    client.publish_messages("topic", "payload")
    assert len(client.message_store) == 1


def test_mqttclient_publish_messages_success(mocker):
    mock_publish = mocker.patch("paho.mqtt.client.Client.publish")
    mock_info = mocker.Mock()
    mock_info.rc = 0
    mock_publish.return_value = mock_info
    client = MqttClient("broker", 1883, "cid", None, None, None)
    client.publish_messages("topic", "payload")
    assert len(client.message_store) == 0
    mock_info.wait_for_publish.assert_called_once()


def test_mqttclient_resend_messages(mocker):
    mock_publish_messages = mocker.patch.object(MqttClient, "publish_messages")
    client = MqttClient("broker", 1883, "cid", None, None, None)
    client.message_store.add_message("topic", "payload")
    client.resend_messages()
    mock_publish_messages.assert_called_with("topic", "payload", 0.05)
