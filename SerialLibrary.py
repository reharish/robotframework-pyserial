# pylint: disable=C0103
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
Author: reharish
Requirements: robotframework, pyserial
"""

from io import BytesIO

import serial

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

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self, unicode='utf-8'):
        """
        Initializes the Serial Library.

        ``unicode`` - Unicode encoding for data communication.
        """
        self.device = None
        self.timeout = 10
        self.unicode = unicode
        self.buffer = BytesIO()

    @keyword("Connect")
    def connect_to_serial_url(self, url: str, baudrate: int) -> serial.Serial:
        """
        Connects to a serial device.

        ``url`` - The device name or URL. see: https://pythonhosted.org/pyserial/url_handlers.html#urls

        ``baudrate`` -  The baud rate to use for communication.

        NOTE: baudrate is kept for backwords compatibility.
        === Example ===
        | Connect |   <device>   | <baudrate>
        | Connect | /dev/ttyUSB0 | 115200
        | Connect | spy:///dev/ttyUSB0/file=dump-comms.txt | 115200

        === Returns ===
        The connected serial device object.
        """
        try:
            self.device = serial.serial_for_url(url, do_not_open=True)
            self.device.baudrate = baudrate
            self.device.open()
        except SerialException as exc:
            raise PySerialError(f"Failed to connect {url}: {exc}") from exc
        return self.device

    @keyword("Disconnect")
    def disconnect_from_serial(self):
        """
        Disconnects from the serial device.

        === Example ===
        | Disconnect
        """
        self.device.close()

    @keyword("Set Timeout")
    def set_timeout(self, seconds: int):
        """
        Sets the read timeout for the serial device.

        ``seconds`` - The timeout value in seconds.

        === Example ===
        | Set Timeout  | <seconds>
        | Set Timeout  |  10
        """
        if not self.device:
            raise PySerialError("Device not initialized to set timeout")
        self.device.timeout = seconds

    @keyword("Set Write Timeout")
    def set_write_timeout(self, seconds: int):
        """
        Sets the write timeout for the serial device.

        ``seconds`` - The timeout value in seconds.

        === Example ===
        | Set Write Timeout  | <seconds>
        | Set Write Timeout  |  10
        """
        if not self.device:
            raise PySerialError("Device not connected to set write timeout")
        self.device.write_timeout = seconds

    @keyword("Set Unicode")
    def set_unicode(self, unicode: str):
        """
        Sets the Unicode encoding for data communication.

        ``unicode`` - The Unicode encoding to use.

        === Example ===
        | Set Unicode  | <unicode>
        | Set Unicode  | utf-8
        """
        self.unicode = unicode

    @keyword("Read")
    def read(self) -> str:
        """
        Reads data from the serial device.

        === Example ===
        | Read

        === Returns ===
        The read data as a string.
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

        ``data`` - The data to write.

        === Example ===
        | Write
        """
        if not self.device:
            raise PySerialError("Device not connected to start write")
        try:
            self.device.write(data.encode())
        except SerialException as exc:
            raise PySerialError(f"Failed to write to device: {exc}") from exc

    @keyword("Read until")
    def read_until(self, expected: str, quiet=True) -> str:
        """
        Reads data from the serial device until a specified string is encountered.

        ``expected`` - The string to read until.

        === Example ===
        | Read until  | <expected>
        | Read until  | string   quiet=False

        === Returns ===
        The read data as a string.
        If the expected not found in the read data, It throws error.
        """
        if not self.device:
            raise PySerialError("Device not connected to start read")
        expected = expected.encode()
        buff = self.device.read_until(expected)
        self.buffer.write(buff)
        data = buff.decode(self.unicode)
        if quiet or expected in buff.decode(self.unicode):
            return data
        raise PySerialError(f"Expected: {expected} not in {data}")

    @keyword("Read all")
    def read_all(self) -> str:
        """
        Reads all the data available in the buffer

        === Example ===
        | Read All

        === Returns ===
        The read data as a string.
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

        === Example ===
        | Reset Input Buffer
        """
        if not self.device:
            raise PySerialError("Device not connected to reset buffer")
        self.device.reset_input_buffer()

    @keyword("Reset Output Buffer")
    def reset_output_buffer(self):
        """
        Clear the output buffer for the serial device

        === Example ===
        | Reset Output Buffer
        """
        if not self.device:
            raise PySerialError("Device not connected to reset buffer")
        self.device.reset_output_buffer()

    @keyword("Close")
    def close_connection(self):
        """
        Closes the connection to the serial device.

        === Example ===
        | Close
        """
        if self.device:
            self.device.close()
            self.device = None

    @keyword("Save buffer to file")
    def save_into_file(self, outputfile: str):
        """
        Saves the data buffer into a file.

        ``outputfile`` - The path to the output file.

        === Example ===
        | Save buffer to file  | <outputfile>
        | Save buffer to file  | test.log
        """
        self.set_timeout(10)
        self.read_all()
        with open(outputfile, 'wb+') as outf:
            outf.write(self.buffer.getvalue())
        print(f"File saved: {outputfile}")
