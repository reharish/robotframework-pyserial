# PySerial - Robot Framework Library

## Overview

PySerial Robot Framework Library is a Python library for interacting with serial devices using Robot Framework. This library provides keywords for connecting to serial devices, reading and writing data, setting timeouts, and more.

## Installation

```bash
pip install robotframework-pyserial
```

## Usage

To use the PySerial Robot Framework Library in your Robot Framework test suites, you need to import it at the beginning of your test suite file:

```robot
*** Settings ***
Library    Serial

*** Test Cases ***
Example Test
    Connect to Serial    COM1    9600
    Set Timeout    5
    Write    Hello, world!
    ${data}=    Read
    Should Be Equal    ${data}    Hello, world!
    Disconnect from Serial
```

## Keywords

- **Connect to Serial**: Connects to a serial device.
- **Disconnect from Serial**: Disconnects from the serial device.
- **Set Timeout**: Sets the read timeout for the serial device.
- **Set Write Timeout**: Sets the write timeout for the serial device.
- **Set Unicode**: Sets the Unicode encoding for data communication.
- **Read**: Reads data from the serial device.
- **Write**: Writes data to the serial device.
- **Read until**: Reads data from the serial device until a specified string is encountered.
- **Read All**: Reads all the data from the input buffer
- **Reset Input Buffer**: Clear the input buffer for the serial device
- **Reset Output Buffer**: Clear the output buffer for the serial device
- **Save buffer to file**: Saves the data buffer into a file.

## Documentation

For detailed documentation of each keyword and usage examples, refer to the documentation in the source code.

## License

APACHE 2.0 - See the LICENSE file for details.
