import socket
import string
import time

# Dummy client code

class Test():
    	def __init__(self):
		self.ip = "192.168.12.21" # Connecting to IP address of MDPGrp2
		self.port = 5182

		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((self.ip, self.port))

# Send data
	def write(self,  msg):
		self.client_socket.send(msg)
		print("sending: ", msg)
		return

	# Receive data
	def receive(self):
		while True:
			data = self.client_socket.recv(47104)
			if (len(data) == 0):
				print ("no data, sorry")
			elif(data == "q"):
				print "quitting.."
				break
			else:
				print("Data received: %s " % data)
				return data