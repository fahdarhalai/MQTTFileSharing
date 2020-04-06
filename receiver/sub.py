import paho.mqtt.client as mqtt

# print("-------------------WELCOME-------------------")
# print("In order to receive the file you must enter")
# print("the same key the sender used in transmition.")
# print("---------------------------------------------")

# key = input("Enter the private key: ")
# filename = input("Give the file a name(with ext): ")

filename = "nofilename"

def on_connect(client, userdata, flags, rc):
    client.subscribe("/tqudqWQBjH/file")
    client.subscribe("/tqudqWQBjH/filename")

def on_message(client, userdata, message):
	global filename
	if message.topic == "/tqudqWQBjH/filename":
		filename=message.payload
	elif message.topic == "/tqudqWQBjH/file":
		file=open(filename,"wb")
		file.write(message.payload)
		file.close()
		filename = "nofilename"
		mqttc.loop_stop()
		exit()

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.connect("mqtt.eclipse.org",1883,60)
mqttc.loop_forever()