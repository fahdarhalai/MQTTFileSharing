import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import os, math, json, re

print("\n\n")
print("███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ ")
print("██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗")
print("███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝")
print("╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗")
print("███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║")
print("╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝")
print("\n\n")
print("---------------------WELCOME---------------------")
print("Make sure the file you are about to transmit is")
print("         located in the same directory.")
print("-------------------------------------------------")

pattern = re.compile(".*[+#].*")

key = ""
while bool(pattern.match(key)) or key == "":
	key = input("Enter a non empty private key: ")

fileTopic = "/{0}/file".format(key)
fileinfoTopic = "/{0}/fileinfo".format(key)
senderChannelTopic = "/{0}/senderChannel".format(key)
receiverChannelTopic = "/{0}/receiverChannel".format(key)

def on_connect(client, userdata, flags, rc):
    client.subscribe(senderChannelTopic)
    print("Waiting for the receiver to connect...")

def on_message(client, userdata, message):
	if message.topic == senderChannelTopic:
		msg = str(message.payload.decode("utf-8","ignore"))
		if msg == "0":
			print("Receiver is connected.")
			publish.single(receiverChannelTopic, "0", hostname="mqtt.eclipse.org")
			transmit()
		elif msg == "1":
			print("SUCCESS")
			exit()

def transmit():
	counter = 1
	fileinfo = {}
	filename = input("Enter filename with extension: ")
	f=open(filename, "rb") 
	print("File opened.")

	filesize = round(os.stat(filename).st_size / 1024.0, 2)
	nbrChunks = math.ceil(os.stat(filename).st_size / 10240)

	fileinfo["name"] = os.path.basename(filename)
	fileinfo["size"] = filesize
	fileinfo["chunks"] = nbrChunks

	print("Sending file info...")
	publish.single(fileinfoTopic, json.dumps(fileinfo), hostname="mqtt.eclipse.org")

	print("Starting file data transmission")
	fileContent = f.read(10240)
	while(fileContent):
		byteArr = bytearray(fileContent)

		print("\tSending chunk ({0})...".format(counter))
		publish.single(fileTopic, byteArr, hostname="mqtt.eclipse.org")

		fileContent = f.read(10240)
		counter += 1

	print("File sent successfully!")
	publish.single(receiverChannelTopic, "1", hostname="mqtt.eclipse.org")
	print("Waiting for receiver AKN...")

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.connect("mqtt.eclipse.org",1883,60)
mqttc.loop_forever()