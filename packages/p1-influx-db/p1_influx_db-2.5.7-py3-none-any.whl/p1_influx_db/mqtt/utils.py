from loguru import logger


def format_message(topic, payload):
    return {"topic": topic, "payload": payload}


def handle_mqtt_error(client, userdata, msg):
    logger.error(f"MQTT Error: {msg}")


def validate_message_format(message):
    if not isinstance(message, dict) or "topic" not in message or "payload" not in message:
        raise ValueError("Invalid message format. Must be a dict with 'topic' and 'payload' keys.")
