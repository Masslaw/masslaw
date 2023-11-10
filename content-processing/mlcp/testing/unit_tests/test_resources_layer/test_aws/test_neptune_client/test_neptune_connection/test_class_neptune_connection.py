import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from resources_layer.aws.neptune_client._neptune_connection import NeptuneConnection


class TestClassNeptuneConnection(unittest.TestCase):

    @patch("resources_layer.aws.neptune_client._neptune_connection.sleep", side_effect=None)
    @patch("resources_layer.aws.neptune_client._neptune_connection.DriverRemoteConnection", autospec=True)
    def test_establish_connection_success(self, mock_driver, mock_sleep):
        mock_connection = MagicMock()
        mock_connection.is_closed.return_value = False
        mock_driver.return_value = mock_connection

        conn = NeptuneConnection("localhost")
        conn.establish_connection()

        self.assertTrue(conn._connected())

    @patch("resources_layer.aws.neptune_client._neptune_connection.sleep", side_effect=None)
    @patch("resources_layer.aws.neptune_client._neptune_connection.DriverRemoteConnection", autospec=True)
    def test_establish_connection_failure(self, mock_driver, mock_sleep):
        mock_driver.side_effect = Exception("Connection failed")

        conn = NeptuneConnection("localhost")

        with self.assertRaises(ConnectionError):
            conn.establish_connection()

        self.assertEqual(mock_sleep.call_count, 3)

    @patch("resources_layer.aws.neptune_client._neptune_connection.DriverRemoteConnection", autospec=True)
    def test_get_connection_without_existing_connection(self, mock_driver):
        mock_connection = MagicMock()
        mock_connection.is_closed.return_value = False
        mock_driver.return_value = mock_connection

        conn = NeptuneConnection("localhost")
        connection = conn.get_connection()

        self.assertTrue(conn._connected())
        self.assertEqual(connection, mock_connection)

    @patch("resources_layer.aws.neptune_client._neptune_connection.DriverRemoteConnection", autospec=True)
    def test_close_connection_existing(self, mock_driver):
        mock_connection = MagicMock()
        mock_connection.is_closed.return_value = False
        mock_driver.return_value = mock_connection

        conn = NeptuneConnection("localhost")
        conn.establish_connection()
        conn.close_connection()

        self.assertIsNone(conn._connection)
        mock_connection.close.assert_called_once()

    @patch("resources_layer.aws.neptune_client._neptune_connection.DriverRemoteConnection", autospec=True)
    def test_close_connection_no_existing(self, mock_driver):
        conn = NeptuneConnection("localhost")
        conn.close_connection()

        self.assertIsNone(conn._connection)
