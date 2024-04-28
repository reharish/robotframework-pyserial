#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Author: reharish@github
Requirements: robotframework, pyserial
"""

import serial

from io import BytesIO

from serial import SerialException
from robot.api.deco import keyword

class PySerialError(Exception):
    """Represents the Serial exceptions"""

class SerialLibrary:
    """
    Library for interacting with serial devices.

    == Example ==

    | Serial.Connect | /dev/ttyUSB0 | 115200
    | Serial.Write   | Hello
    | ${DATA}=       | Serial.Read
    | ${DATA}=       | Serial.Read All
    | Serial.Save Buffer to file |  /path/to/serial.log

    == Another Example ==

    | Connect     | /dev/ttyUSB1 | 115200
    | Set Timeout | 2
    | Reset Input Buffer
    | Reset Output Buffer
    | Write       | Hello
    | Write       | Hello
    | Read until  | World
    | Read All

    """

    ROBOT_AUTO_KEYWORDS = False

    def __init__(self, unicode='utf-8'):
        """
        Initializes the Serial Library.

        Arguments
        - unicode - Unicode encoding for data communication.
        """
        self.device = None
        self.timeout = 10
        self.unicode = unicode
        self.buffer = BytesIO()

    @keyword("Connect")
    def connect_to_serial(self, device: str, baudrate: int) -> serial.Serial:
        """
        Connects to a serial device.

        Arguments:
        - device: The device name or a device number.
        - baudrate: The baud rate to use for communication.

        Returns:
        - The connected serial device object.
        """
        try:
            self.device = serial.Serial(device, baudrate=baudrate)
        except SerialException as exc:
            raise PySerialError(f"Failed to connect {device}: {exc}")
        return self.device

    @keyword("Disconnect")
    def disconnect_from_serial(self):
        """
        Disconnects from the serial device.
        """
        self.device.close()

    @keyword("Set Timeout")
    def set_timeout(self, seconds: int):
        """
        Sets the read timeout for the serial device.

        Arguments:
        - seconds: The timeout value in seconds.
        """
        if not self.device:
            raise PySerialError("Device not initialized to set timeout")
        self.device.timeout = seconds

    @keyword("Set Write Timeout")
    def set_timeout_write(self, seconds: int):
        """
        Sets the write timeout for the serial device.

        Arguments:
        - seconds: The timeout value in seconds.
        """
        if not self.device:
            raise PySerialError("Device not connected to set write timeout")
        self.device.write_timeout = seconds

    @keyword("Set Unicode")
    def set_unicode(self, unicode: str):
        """
        Sets the Unicode encoding for data communication.

        Arguments:
        - unicode: The Unicode encoding to use.
        """
        self.unicode = unicode

    @keyword("Read")
    def read(self) -> str:
        """
        Reads data from the serial device.

        Returns:
        - The read data as a string.
        """
        if not self.device:
            raise PySerialError("Device not connected to start read")
        buff = self.device.read()
        self.buffer.write(buff)
        buff = buff.decode(self.unicode)
        return buff

    @keyword("Write")
    def write(self, data: str):
        """
        Writes data to the serial device.

        Arguments:
        - data: The data to write.
        """
        if not self.device:
            raise PySerialError("Device not connected to start write")
        try:
            self.device.write(data.encode())
        except SerialException as exc:
            raise PySerialError(f"Failed to write to device: {exc}")

    @keyword("Read until")
    def read_until(self, expected: str) -> str:
        """
        Reads data from the serial device until a specified string is encountered.

        Arguments:
        - expected: The string to read until.

        Returns:
        - The read data as a string.
        """
        if not self.device:
            raise PySerialError("Device not connected to start read")
        expected = expected.encode()
        buff = self.device.read_until(expected)
        self.buffer.write(buff)
        return buff.decode(self.unicode)

    @keyword("Read All")
    def read_all(self):
        """
        Reads all the data available in the buffer
        
        Returns:
        - The read data as a string.
        """
        if not self.device:
            raise PySerialError("Device not connected to start read")
        buff = self.device.read_all()
        self.buffer.write(buff)
        return buff.decode(self.unicode)

    @keyword("Reset Input Buffer")
    def reset_input_buffer(self):
        """
        Clear the input buffer for the serial device
        """
        if not self.device:
            raise PySerialError("Device not connected to reset buffer")
        self.device.reset_input_buffer()
        return

    @keyword("Reset Output Buffer")
    def reset_output_buffer(self):
        """
        Clear the output buffer for the serial device
        """
        if not self.device:
            raise PySerialError("Device not connected to reset buffer")
        self.device.reset_output_buffer()
        return

    @keyword("Close")
    def close_connection(self):
        """
        Closes the connection to the serial device.
        """
        if self.device:
            self.device.close()
            self.device = None

    @keyword("Save buffer to file")
    def save_into_file(self, outputfile: str):
        """
        Saves the data buffer into a file.

        Arguments:
        - outputfile: The path to the output file.
        """
        self.set_timeout(10)
        self.read_all()
        with open(outputfile, 'wb+') as outf:
            outf.write(self.buffer.getvalue())
        print(f"File saved: {outputfile}")
