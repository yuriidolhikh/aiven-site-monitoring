import json
import kafka
import logging
import psycopg2

from aiven.utils.log_utils import get_logger

logger = get_logger("consumer")


class Consumer:
    """
        Site monitoring message consumer class.
        Reads data from Kafka topic and stores it in PostgreSQL DB
    """
    def __init__(self, config: dict) -> None:
        try:
            self._consumer = kafka.KafkaConsumer(
                config['kafka']['topic'],
                auto_offset_reset="earliest",
                bootstrap_servers=config['kafka']['uri'],
                security_protocol="SSL",
                group_id="site-availability-group",
                ssl_cafile="keys/ca.pem",
                ssl_certfile="keys/service.cert",
                ssl_keyfile="keys/service.key",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                enable_auto_commit=True
            )
        except kafka.errors.NoBrokersAvailable:
            raise Exception(f"Unable to connect to Kafka at {config['kafka']['uri']}")

        # Init PostgreSQL connection and do some sanity checking
        try:
            conn = psycopg2.connect(**config['postgres'])
            conn.autocommit = True
            self._conn = conn
        except psycopg2.OperationalError:
            raise Exception(f"Unable to connect to PostgreSQL instance at {config}")

        # Simple check to ensure that our working table exists
        with self._conn.cursor() as cur:
            try:
                cur.execute('SELECT 1 FROM availability_data')
            except psycopg2.errors.UndefinedTable:
                raise Exception("'availability_data' table does not exist. Please create it using supplied schema.sql")

    def consume(self) -> None:
        """Continuously poll topic and write data to PostgreSQL"""
        for msg in self._consumer:
            logger.info(f"Received message: {msg.value}")
            with self._conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO
                        availability_data (host, status_code, elapsed_time, regex_matched)
                    VALUES
                        (%(host)s, %(status_code)s, %(elapsed_time)s, %(regex_matched)s)
                """, msg.value)


if __name__ == "__main__":
    with open("conf/config.json", "r") as f:
        config = json.load(f)

    c = Consumer(config['persistence'])
    c.consume()
