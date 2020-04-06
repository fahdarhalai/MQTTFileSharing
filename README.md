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
1. Install paho-mqtt package:<br>
```pip install paho-mqtt```
2. Clone the repository:<br>
```git clone https://github.com/fahdarhalai/MQTTFileSharing```
3. Run the scripts in different terminals or in different machines(no order is required):<br>
```python sender.py```<br>
```python receiver.py```<br>
You will be prompted to enter a private key(should not contain '+' or '#' characters), it is used to make sure that only the receiver who has the same key, will be allowed to receive the file.
## Test
Running both scripts on my machine:
<p align="center">
  <img src="https://user-images.githubusercontent.com/41004675/78612597-a2fef480-7861-11ea-8339-47c7ebfdab35.PNG" align="middle" width="85%">
</p>

Running the receiver script on my phone using Termux terminal emulator:
<p align="center">
  <img src="https://user-images.githubusercontent.com/41004675/78612990-9929c100-7862-11ea-9cfc-b65d0bdbd77d.jpg" align="middle" width="65%">
  <br>
  <img src="https://user-images.githubusercontent.com/41004675/78612996-9dee7500-7862-11ea-93fa-c1677009ea97.jpg" align="middle" width="65%">
</p>
