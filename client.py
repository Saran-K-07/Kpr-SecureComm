import socket
import threading

PORT = 5050 
HEADER = 64
FORMAT = "utf-8"
# SERVER = socket.gethostbyname(socket.gethostname())

SERVER = "127.0.0.2"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE="!DISCONNECT"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg) :
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER -len(send_length))
	client.send(send_length)
	client.send(message)


out= 1
while out :
	txt=input()
	
	if(txt== "quit" ):
		send(DISCONNECT_MESSAGE)
		out=0
	else :
		send(txt)
		
	

