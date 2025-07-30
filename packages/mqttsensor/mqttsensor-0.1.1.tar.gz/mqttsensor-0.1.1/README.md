# mqttsensor

A Python package for sending sensor data over MQTT with message persistence and reconnection support.

## Features

- MQTT client with TLS support
- Automatic message storage and resend on connection loss
- Configurable via TOML file
- Logging with loguru

## Installation

```bash
pip install .
```

## Configuration

Create a `config.toml` file in your project directory:

```toml
[mqtt]
broker = "localhost"
port = 1883
client_id = "your_client_id"
ca_certs = "ca.pem"
certfile = "cert.pem"
key = "key.pem"
max_times = 3
```

## Usage

```python
from mqttsensor.main import init_client

config, mqtt_client = init_client("config.toml")
mqtt_client.start()
# Send sensor data
mqtt_client.send_sensor_data(
    measurement="temperature",
    location="office",
    sensor_id="sensor01",
    unit="C",
    value=23.5
)
mqtt_client.stop()
```

## Testing

Run all tests with:

```bash
pytest
```

## License

MIT License