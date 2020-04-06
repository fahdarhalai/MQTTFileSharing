import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time, json
import _thread as thread
import re

print("\n\n")
print("██████╗ ███████╗ ██████╗███████╗██╗██╗   ██╗███████╗██████╗ ")
print("██╔══██╗██╔════╝██╔════╝██╔════╝██║██║   ██║██╔════╝██╔══██╗")
print("██████╔╝█████╗  ██║     █████╗  ██║██║   ██║█████╗  ██████╔╝")
print("██╔══██╗██╔══╝  ██║     ██╔══╝  ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗")
print("██║  ██║███████╗╚██████╗███████╗██║ ╚████╔╝ ███████╗██║  ██║")
print("╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝")
print("\n\n")
print("---------------------------WELCOME--------------------------")
print("In order to receive the file you must have the same exact")
print("         key the sender used while trasmitting.")
print("------------------------------------------------------------")

pattern = re.compile(".*[+#].*")

key = ""
while bool(pattern.match(key)) or key == "":
	key = input("Enter a non empty private key: ")


fileTopic = "/{0}/file".format(key)
fileinfoTopic = "/{0}/fileinfo".format(key)
receiverChannelTopic = "/{0}/receiverChannel".format(key)
senderChannelTopic = "/{0}/senderChannel".format(key)

filename = "nofilename"
file = None
cnx = False
counter = 1
sent = False

def establish_connection(threadName, delay):
	print("Waiting for sender to connect...")
	while not cnx:
		mqttc.publish(senderChannelTopic, "0")
		time.sleep(delay)

def on_connect(client, userdata, flags, rc):
    client.subscribe(fileTopic)
    client.subscribe(fileinfoTopic)
    client.subscribe(receiverChannelTopic)
    

def on_message(client, userdata, message):
	global filename
	global file
	global cnx
	global counter

	if message.topic == receiverChannelTopic:
		msg = str(message.payload.decode("utf-8","ignore"))
		if msg == "0":
			print("Sender connected.")
			cnx = True
		elif msg == "1":
			print("File received successfully!")
			publish.single(senderChannelTopic, "1", hostname="mqtt.eclipse.org")
			file.close()
			exit()

	elif message.topic == fileinfoTopic:
		print("File Info:")
		fileinfo=json.loads(message.payload.decode("utf-8", "ignore"))
		print(" - Name : {0}\n - Size : {1} KB\n - Number of chunks : {2}".format(fileinfo["name"], fileinfo["size"], fileinfo["chunks"]))
		filename=fileinfo['name']
		print("Begin file writing...")
		file=open(filename, "wb")

	elif message.topic == fileTopic:
		print("\tReceiving chunk ({0})...".format(counter))
		file.write(message.payload)
		counter += 1

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.connect("mqtt.eclipse.org",1883,60)

thread.start_new_thread(establish_connection, ("Connection-Establish", 5))

mqttc.loop_forever()

