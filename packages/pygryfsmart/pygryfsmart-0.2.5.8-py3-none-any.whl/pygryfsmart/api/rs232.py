import serial
import logging

_LOGGER = logging.getLogger(__name__)

class RS232Handler:
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

    def _connect(self):
        try:
            if self.serial_conn is None or not self.serial_conn.is_open:
                self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
                _LOGGER.info(f"Connected to {self.port}")
        except serial.SerialException as e:
            _LOGGER.warning(f"Could not open port {self.port}: {e}")
            self.serial_conn = None

    async def open_connection(self):
        self._connect()

    async def close_connection(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            _LOGGER.info(f"Connection to {self.port} closed.")
        self.serial_conn = None

    async def send_data(self, data: str):
        self._connect()
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(data.encode('utf-8'))
                _LOGGER.debug(f"Sent: {data.strip()}")
            except serial.SerialException as e:
                _LOGGER.error(f"Send error: {e}")
                await self.close_connection()

    async def read_data(self) -> str:
        self._connect()
        if self.serial_conn and self.serial_conn.is_open:
            try:
                data = self.serial_conn.readline().decode('utf-8').strip()
                _LOGGER.debug(f"Received: {data}")
                return data
            except serial.SerialException as e:
                _LOGGER.error(f"Read error: {e}")
                await self.close_connection()
        return ""

