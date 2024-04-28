*** Settings ***
Library  Serial

Suite Teardown  Save buffer into file  serial.log

*** Test Cases ***
Basic Read and Write
    Serial.Connect  /dev/ttyUSB0  115200
    Serial.Set Timeout  ${5}
    Serial.Reset Input Buffer
    Serial.Reset Output Buffer
    Serial.Write  Hello
    Serial.Read
