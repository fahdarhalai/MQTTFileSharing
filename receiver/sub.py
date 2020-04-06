import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import _thread as thread

print("-------------------WELCOME-------------------")
print("In order to receive the file you must have")
print("the same key the sender used in transmition.")
print("---------------------------------------------")

# key = input("Enter the private key: ")

filename = "nofilename"
file = None
cnx = False
counter = 1
sent = False

def establish_connection(threadName, delay):
	print("Waiting for sender to connect...")
	while not cnx:
		mqttc.publish("/tqudqWQBjH/senderChannel", "0")
		time.sleep(delay)

def on_connect(client, userdata, flags, rc):
    client.subscribe("/tqudqWQBjH/file")
    client.subscribe("/tqudqWQBjH/filename")
    client.subscribe("/tqudqWQBjH/receiverChannel")
    

def on_message(client, userdata, message):
	global filename
	global file
	global cnx
	global counter

	if message.topic == "/tqudqWQBjH/receiverChannel":
		msg = str(message.payload.decode("utf-8","ignore"))
		if msg == "0":
			print("Sender connected.")
			cnx = True
		elif msg == "1":
			print("File received successfully!")
			publish.single("/tqudqWQBjH/senderChannel", "1", hostname="mqtt.eclipse.org")
			file.close()
			exit()

	elif message.topic == "/tqudqWQBjH/filename":
		print("Filename received.")
		filename=message.payload
		print("Begin file writing...")
		file=open(filename,"wb")

	elif message.topic == "/tqudqWQBjH/file":
		print("\tReceiving chunk ({0})...".format(counter))
		file.write(message.payload)
		counter += 1

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.connect("mqtt.eclipse.org",1883,60)

thread.start_new_thread(establish_connection, ("Connection-Establish", 5))

mqttc.loop_forever()

