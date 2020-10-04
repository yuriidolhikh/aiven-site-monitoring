from unittest import mock

from aiven.consumer import Consumer


class KafkaMessage:
    def __init__(self, value):
        self.value = value


def test_consume():

    with mock.patch('psycopg2.connect'), mock.patch('kafka.KafkaConsumer'):

        c = Consumer({'kafka': {'topic': 'test', 'uri': 'test'}, 'postgres': {}})
        c._conn.cursor().__enter__().execute.assert_called_with("SELECT 1 FROM availability_data"),\
            "Main table existence was not checked"

        message = KafkaMessage({
            'host': 'example.com',
            'status_code': 200,
            'elapsed_time': 111.02,
            'regex_matched': True
        })
        c._consumer.__iter__.return_value = [message]
        c.consume()

        # Test message consumption
        assert c._consumer.__iter__.called, "Kafka queue was not polled"
        assert c._conn.cursor().__enter__().execute.call_args_list[1][0][1]\
            == {'host': 'example.com', 'status_code': 200, 'elapsed_time': 111.02, 'regex_matched': True},\
            "DB insertion with unexpected parameters"