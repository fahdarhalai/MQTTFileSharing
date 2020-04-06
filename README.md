# MQTTFileSharing
MQTT File Sharing scripts (receiver script &amp; sender script) written in Python

## Introduction
This project is a small file sharing system, that uses MQTT protocol to share binary data over internet. The MQTT broker is provided by eclipse, and can be accessed at mqtt.eclipse.org on port 1883 over unencrypted TCP (or 8883 for communication over encrypted TCP). Any MQTT broker can be a good replacement since the eclipse public broker is little bit slow.

The file sharing is performed in the following steps:
- From sender's view point:
  - Waiting for the receiver to connect
  - Opening the file
  - Sending file information (name, size, number of chunks)
  - Reading the file in chunks of 10KB
  - Sending each chunk alone
  - Sending the transmission completion aknowledgement
  - Receiving the receipt aknowledgement
- From receiver's view point:
  - Waiting for the sender to connect
  - Receiving file information
  - Creating a new file
  - Receiving each chunk
  - Writing each chunk in the file
  - Receiving the transmission completion aknowledgement
  - Sending the receipt aknowledgement
## Setup
In order to work with MQTT, you must first download the ```paho-mqtt``` package:
```
pip install paho-mqtt
```
Now you can clone my repository using the ```git clone``` command. Run the sender's script, and the receiver's script (the order doesn't matter). You will be prompted to enter a private key, it is used to make sure that only the receiver who has the same key, will be able to receive the file.
## Test
