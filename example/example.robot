*** Settings ***
Library  Serial


*** Test Cases ***
Read and Write Test
    Serial.Connect  /dev/ttyUSB0  115200
    Serial.Read
    Serial.Write
