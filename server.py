import socket
import threading

PORT = 5050 

SERVER = "127.0.0.2"
HEADER = 64
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
DISCONNECT_MESSAGE="!DISCONNECT"

server.bind(ADDR)

def handle_client(conn,address) :
	print(f"[NEW CONNECTION] {address} connected ")
	connected=True
	while connected :
		msg_length=conn.recv(HEADER).decode(FORMAT)
		if msg_length :
			msg_length=int(msg_length)	
			msg=conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE :
				connected=False

			print(f"[{address}] {msg}")
	conn.close()	



def start():
	server.listen()
	print(f"[LISTENING] server is listening on {SERVER} ")
	while True :
		connection,address=server.accept()
		thread=threading.Thread(target=handle_client,args=(connection,address))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] server is starting .... ")
start()

