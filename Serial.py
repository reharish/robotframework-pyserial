from io import BytesIO

import serial
from serial import SerialException

from robot.api.deco import library
from robot.api.deco import keyword

class PySerialError(Exception):
    """Represents the Serial expections"""

class Serial:
    def __init__(self):
        self.device = None
        self.timeout =  10
        self.unicode = 'latin-1'
        self.buffer = BytesIO()

    @keyword("Connect")
    def connect_to_serial(self, device: str, baudrate: int) -> serial.Serial:
        """
        FIXME:
        """
        try:
            self.device = serial.Serial(device, baudrate=baudrate)
        except SerialException as exc:
            raise PySerialError(f"Failed to connect {device}: {exc}")
        return self.device

    @keyword("Disconnect")
    def disconnect_from_serial(self):
        self.device.disconnect()

    @keyword("Set Timeout")
    def set_timeout(self, seconds:int):
        """
        seconds
        """
        if not self.device:
            raise PySerialError("Device not intialized to set timeout")
        self.device.timeout = seconds
        return

    @keyword("Set Write Timeout")
    def set_write_timeout(self, seconds:int):
        """
        """
        if not self.device:
            raise PySerialError("Device not connected to set write timeout")
        self.device.write_timeout = seconds
        return

    @keyword("Set Unicode")
    def set_unicode(self, unicode: str):
        """
        """
        self.unicode = unicode
        return

    @keyword("Read")
    def read(self) -> str:
        if not self.device:
            raise PySerialError("Device not connected to start read")
        buff = self.device.read()
        self.buffer.write(buff)
        buff = buff.decode(self.unicode)
        return buff

    @keyword("Write")
    def write(self, data: str):
        if not self.device:
            raise PySerialError("Device not connected to start read")
        self.write(data.encode())
        return

    @keyword("Read until")
    def read_until(self, expected: str) -> str:
        """
        """
        if not self.device:
            raise PySerialError("Device not connected to start read")
        expected = expected.encode()
        buff = self.device.read_until(expected.encode())
        self.buffer.write(buff)
        return buff.decode(self.unicode)

    @keyword("Save buffer into file")
    def save_into_file(self, outputfile: str):
        """
        """
        self.set_timeout(10)
        buff = self.device.read()
        self.buffer.write(buff)
        with open(outputfile, 'wb+') as outf:
            outf.write(self.buffer.read())
        print(f"File saved: {outputfile}")
        return
