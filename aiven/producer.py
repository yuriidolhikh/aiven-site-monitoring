import json
import kafka
import re
import requests
import threading
import time

from aiven.utils.log_utils import get_logger


logger = get_logger("producer")


def monitor(producer: kafka.KafkaProducer, topic: str, target: str, regex: str) -> None:
    """Monitor target site and send results to Kafka"""
    try:
        logger.debug(f"Checking {target}")
        r = requests.get(target)
        elapsed = r.elapsed.microseconds / 1000
        message = {
            "host": target,
            "status_code": r.status_code,
            "elapsed_time": elapsed,
            "regex_matched": bool(re.search(regex, r.text)) if regex else None
        }

        logger.info(f"Sending message to Kafka: {message}")
        producer.send(topic, message)
    except Exception as e:
        logger.error(f"Check failed: {e}")

def run(producer: kafka.KafkaProducer, topic: str, target: str, interval: int, regex: str) -> None:
    """Wrapper for threaded run"""
    while True:
        monitor(producer, topic, target, regex)
        time.sleep(interval)

if __name__ == "__main__":
    with open("conf/config.json", "r") as f:
        config = json.load(f)

    try:
        producer = kafka.KafkaProducer(
            bootstrap_servers=config['persistence']['kafka']['uri'],
            security_protocol="SSL",
            ssl_cafile="keys/ca.pem",
            ssl_certfile="keys/service.cert",
            ssl_keyfile="keys/service.key",
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
    except kafka.errors.NoBrokersAvailable:
        raise Exception(f"Unable to connect to Kafka at {config['persistence']['kafka']['uri']}")

    # Start all monitoring threads
    topic = config['persistence']['kafka']['topic']
    [
        threading.Thread(target=run, args=(producer, topic, target, params['interval'], params['regex'])).start()
        for target, params in config['monitoring'].items()
    ]
