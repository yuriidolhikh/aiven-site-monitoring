from datetime import timedelta
from unittest import mock

from aiven.producer import monitor


def test_monitoring():
    with mock.patch('requests.get') as mocked_get:

        mocked_kafka = mock.MagicMock()
        mocked_response = mock.MagicMock()

        mocked_response.status_code = 200
        mocked_response.elapsed = timedelta(microseconds=88000)
        mocked_response.text = "test html"

        mocked_get.return_value = mocked_response

        monitor(mocked_kafka, "test", "http://example.com", "html")

        mocked_get.assert_called_with("http://example.com")
        mocked_kafka.send.assert_called_with('test',
            {'host': 'http://example.com', 'status_code': 200, 'elapsed_time': 88.0, 'regex_matched': True}
        )