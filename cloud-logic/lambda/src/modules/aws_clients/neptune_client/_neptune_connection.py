import logging
import os

from time import sleep

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class NeptuneConnection:
    def __init__(self, connection_endpoint, connection_protocol="ws", connection_port=8182, connection_type='gremlin'):
        self.logger = logging.getLogger(os.environ['FUNCTION_NAME'])
        self.logger.info(f"Creating a new Neptune connection. protocol: {connection_protocol} endpoint: {connection_endpoint} port: {connection_port} type: {connection_type}")
        self._connection_protocol = connection_protocol
        self._connection_endpoint = connection_endpoint
        self._connection_port = connection_port
        self._connection_type = connection_type
        self._connection = None

    def establish_connection(self):
        for _ in range(3):
            try:
                self._connection = DriverRemoteConnection(f"{self._connection_protocol}://{self._connection_endpoint}:{self._connection_port}/{self._connection_type}", 'g')
                assert (self._connected())
                self.logger.info("Connection Established Successfully")
                return
            except Exception as e:
                self.logger.info(f"Failed trying to connect to Neptune: {e}")
                self.logger.info("Retrying in 1 seconds...")
                sleep(1)
        raise ConnectionError("Failed trying to connect to Neptune")

    def get_connection(self):
        self._ensure_connection()
        return self._connection

    def close_connection(self):
        if not self._connected():
            self._connection = None
            return
        self._connection.close()
        self._connection = None
        self.logger.info("Connection Closed")

    def _ensure_connection(self):
        if not self._connected():
            self.establish_connection()

    def _connected(self):
        return self._connection is not None and not self._connection.is_closed()
