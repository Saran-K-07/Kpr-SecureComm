import socket
import threading
from user import user

PORT = 5050 

SERVER = "127.0.0.2"
HEADER = 64
# SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER,PORT)
FORMAT = "utf-8"
# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
DISCONNECT_MESSAGE="!DISCONNECT"

# server.bind(ADDR)

class Group :
	def __init__(self,id):
		self.group_id = id
		self.users_list=set()

	def show_members(self) :
		print(self.group_id," : ",self.users_list)

	def add_member(self,user_id) :
		self.users_list.add(user_id)
	def no_of_members(self) :
		return len(self.users_list)

		
		

class Server :
	def __init__(self, server_ip, server_port):
		self.IP = server_ip
		self.PORT = server_port
		self.clientConnections = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ADDR=(self.IP,self.PORT)
		self.user_dict={} #dictionary of user id to user object
		self.group_dict={}


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
		print(f"[NEW CONNECTION] {conn,address} connected ")
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

					if(len(msg_list) != 4 ):
						msg="Error : Please provide proper args"
						self.send(msg,conn)

					else :

						new_user = user(msg_list[1],msg_list[2],msg_list[3],address[0],address[1])
						self.user_dict[msg_list[2]] = new_user
						print("checking new user ",new_user.getIpPort())
						msg="user created succesfully"
						self.send(msg,conn)

				elif msg_list[0] =="LOGIN" :

					if(len(msg_list) != 3 ):
						# print()
						msg="Error : Please provide proper args"
						self.send(msg,conn)
					else :

						
						username = msg_list[1]
						password = msg_list[2]

						try :

							curr_user=self.user_dict[username]
							print("curr_user ",curr_user)
							login_status=curr_user.signIn(username,password)

							if login_status == True :

								print("Logged In succesfully ")
								msg="True"
								self.send(msg,conn)

							else :
								
								msg="False"
								self.send(msg,conn)

						except :
							msg="False"
							self.send(msg,conn)
						
								
				elif msg_list[0] == "SEND" :
					print("Please send the message")
				elif msg_list[0] == "JOIN" :
					print("Please JOIN the group")
					if len(msg_list) != 3 :
						msg="False"
						self.send(msg,conn)
					else :
						if msg_list[2] not in group :
							self.create_group(msg_list[2],msg_list[1],conn)
						else :
							self.group_dict[msg_list[2]].add_member(msg_list[1])
							self.user_dict[msg_list[1]].joinGroup(msg_list[2])
							msg="True"
							self.send(msg,conn)
			


							
						


				elif msg_list[0] == "CREATE" :
					if len(msg_list) != 3 :
						msg="False"
						self.send(msg,conn)
					else :
						self.create_group(msg_list[2],msg_list[1],conn)

					
				elif msg_list[0] == "LIST" :
					groups= list(self.group_dict.keys())
					print("groups ",groups)
					if len(groups) == 0:
						msg = "NO GROUPS"
					else :
						msg=' '.join(groups)
					self.send(msg,conn)



				
		conn.close()	

	def create_group(self,grp,user_id,conn):
		if grp in self.group_dict.keys() :
			msg="False"
			self.send(msg,conn)
		else :
			self.group_dict[grp]=Group(grp)
			self.group_dict[grp].add_member(user_id)
			self.user_dict[user_id].joinGroup(grp)
			msg="True"
			self.send(msg,conn)

						
					
	def send(self,msg,connection) :
		message = msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (HEADER -len(send_length))
		connection.send(send_length)
		connection.send(message)	

    	
    	
   

print("[STARTING] server is starting .... ")
server=Server(SERVER,PORT)
server.server_start()



