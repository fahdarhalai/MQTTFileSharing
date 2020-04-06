import paho.mqtt.publish as publish

print("-------------------WELCOME-------------------")
print("Make sure the file you are about to transmit")
print("is located in the same directory.")
print("---------------------------------------------")

# key = input("Enter the private key: ")
filename = input("Enter filename with extension: ")

f=open(filename, "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)

publish.single("/tqudqWQBjH/filename", filename, hostname="mqtt.eclipse.org")
publish.single("/tqudqWQBjH/file", byteArr, hostname="mqtt.eclipse.org")