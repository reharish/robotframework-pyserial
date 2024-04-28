*** Settings ***
Library  SerialLibrary

Suite Teardown  Save buffer to file  serial.log

*** Test Cases ***
Basic Read and Write
    SerialLibrary.Connect  /dev/ttyUSB0  115200
    SerialLibrary.Set Timeout  ${5}
    SerialLibrary.Reset Input Buffer
    SerialLibrary.Reset Output Buffer
    SerialLibrary.Write  Hello
    SerialLibrary.Read
