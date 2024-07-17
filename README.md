# Robot Framework - SerialLibrary

## Overview

PySerial Robot Framework Library is a Python library for interacting with serial devices using Robot Framework. This library provides keywords for connecting to serial devices, reading and writing data, setting timeouts, and more.

## Installation

![pypi workflow](https://github.com/reharish/robotframework-pyserial/actions/workflows/pypi-package.yml/badge.svg)

```bash
pip install robotframework-pyserial
```


## Documentation

![docs workflow](https://github.com/reharish/robotframework-pyserial/actions/workflows/docs-pages.yml/badge.svg)

For detailed documentation of each keyword and usage examples, refer to the documentation in the below link,

https://reharish.github.io/robotframework-pyserial

## Project Inspiration

- [zilogic-systems/parrot](https://github.com/zilogic-systems/parrot) - Embedded Test Automation Framework, based on Robot Framework.

- [pySerial](https://github.com/pyserial/pyserial) - Python serial port access library

## Usage

To use the PySerial Robot Framework Library in your Robot Framework test suites, you need to import it at the beginning of your test suite file:

```robot
*** Settings ***
Library    SerialLibrary

*** Test Cases ***
Example Test
    Connect        COM1    9600
    Set Timeout    5
    Write          Hello, world!
    ${data}=       Read
    Should Be Equal    ${data}    Hello, world!
    Disconnect from Serial
```

## Keywords

| Keyword                  | Description                                    |
|--------------------------|------------------------------------------------|
| **Connect**              | Connects to a serial device.                   |
| **Disconnect**           | Disconnects from the serial device.            |
| **Set Timeout**          | Sets the read timeout for the serial device.   |
| **Set Write Timeout**    | Sets the write timeout for the serial device.  |
| **Set Unicode**          | Sets the Unicode encoding for data communication. |
| **Read**                 | Reads data from the serial device.             |
| **Write**                | Writes data to the serial device.              |
| **Read until**           | Reads data from the serial device until a specified string is encountered. |
| **Read All**             | Reads all the data from the input buffer.      |
| **Reset Input Buffer**   | Clear the input buffer for the serial device.  |
| **Reset Output Buffer**  | Clear the output buffer for the serial device. |
| **Save buffer to file**  | Saves the data buffer into a file.             |


## Contributors

- Harishbabu Rengaraj([@reharish](https://github.com/reharish))
- Abisheak Kumarasamy ([@abi-sheak](https://github.com/abi-sheak))
- Karl Palsson ([@karlp](https://github.com/karlp))


## License

- See the `LICENSE` file for details.
