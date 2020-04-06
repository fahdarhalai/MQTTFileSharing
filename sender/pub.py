import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

print("-------------------WELCOME-------------------")
print("Make sure the file you are about to transmit")
print("is located in the same directory.")
print("---------------------------------------------")

# key = input("Enter the private key: ")

def on_connect(client, userdata, flags, rc):
    client.subscribe("/tqudqWQBjH/senderChannel")
    print("Waiting for the receiver to connect...")

def on_message(client, userdata, message):
	if message.topic == "/tqudqWQBjH/senderChannel":
		msg = str(message.payload.decode("utf-8","ignore"))
		if msg == "0":
			print("Receiver is connected.")
			publish.single("/tqudqWQBjH/receiverChannel", "0", hostname="mqtt.eclipse.org")
			transmit()
		elif msg == "1":
			print("SUCCESS")
			exit()

def transmit():
	counter = 1
	filename = input("Enter filename with extension: ")
	f=open(filename, "rb") 
	print("File opened!")

	print("Sending filename...")
	publish.single("/tqudqWQBjH/filename", filename, hostname="mqtt.eclipse.org")
	print("Filename sent successfully!")

	print("Starting file data transmission")
	fileContent = f.read(10240)
	while(fileContent):
		byteArr = bytearray(fileContent)

		print("\tSending chunk ({0})...".format(counter))
		publish.single("/tqudqWQBjH/file", byteArr, hostname="mqtt.eclipse.org")
		print("\t\tChunk sent")

		fileContent = f.read(10240)
		counter += 1

	print("File sent successfully!")
	publish.single("/tqudqWQBjH/receiverChannel", "1", hostname="mqtt.eclipse.org")
	print("Waiting for receiver AKN...")

mqttc=mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.connect("mqtt.eclipse.org",1883,60)
mqttc.loop_forever()