import socket
import threading

PORT = 5050 

SERVER = "127.0.0.2"
HEADER = 64
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER,PORT)
FORMAT = "utf-8"
# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
DISCONNECT_MESSAGE="!DISCONNECT"

# server.bind(ADDR)

class Server :
	def __init__(self, server_ip, server_port):
		self.IP = server_ip
		self.PORT = server_port
		self.clientConnections = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ADDR=(self.IP,self.PORT)

	def server_start(self):

		try:
			self.server.bind(self.ADDR)

		except socket.error as e:
			print(str(e))
		self.server.listen(10)
		print(f"[*] Starting server ({self.IP}) on port {self.PORT}")
		while True :
			connection,address=self.server.accept()
			thread=threading.Thread(target=self.handle_client,args=(connection,address))
			thread.start()
			print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


	def handle_client(self,conn,address) :
		print(f"[NEW CONNECTION] {address} connected ")
		connected=True
		while connected :
			msg_length=conn.recv(HEADER).decode(FORMAT)
			if msg_length :
				msg_length=int(msg_length)	
				msg=conn.recv(msg_length).decode(FORMAT)
				if msg == DISCONNECT_MESSAGE :
					connected=False

				msg_list=msg.split()
				print(f"[{address}] {msg_list}")
				if msg_list[0] == "CREATE_USER" :
					print("User has to be created")
				elif msg_list[0] =="LOGIN" :
					print("Please login the user")
				elif msg_list[0] == "SEND" :
					print("Please send the message")
				elif msg_list[0] == "JOIN" :
					print("Please JOIN the group")
				elif msg_list[0] == "CREATE" :
					print("Please CREATE the group")		

					

				
		conn.close()			







print("[STARTING] server is starting .... ")
server=Server(SERVER,PORT)
server.server_start()


