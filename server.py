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


#group class contains a group_id and a list of users who are part of it
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

		
		
#server class to handle all server related works
class Server :
	def __init__(self, server_ip, server_port):
		self.IP = server_ip            #ip of server
		self.PORT = server_port		   #port of server
		self.clientConnections = []    #active connection list of clients connected to this server
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #creating socket object named server
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #setting socket up
		self.ADDR=(self.IP,self.PORT)  #tuple of server ip and server address
		self.user_dict={}              #dictionary of user id to user object
		self.group_dict={}             #dictionary of groupids to list of user objects


	def server_start(self):

		try:
			self.server.bind(self.ADDR)             #binding the created socket to server ip and port (ADDR=(IP,PORT))

		except socket.error as e:
			print(str(e))
		self.server.listen(10)
		print(f"[*] Starting server ({self.IP}) on port {self.PORT}")
		while True :                                
			connection,address=self.server.accept()         #accepting client socket, address(port) from client
			thread=threading.Thread(target=self.handle_client,args=(connection,address))
			thread.start()
			print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


	#Function to handle client requests concurrently (one spawned for every client requesting a connection)
	def handle_client(self,conn,address) :
		print(f"[NEW CONNECTION] {conn,address} connected ")
		connected=True
		while connected :
			msg_length=conn.recv(HEADER).decode(FORMAT)               #receive size of msg from client to handle (put in buffer size of HEADER(64 B))
			if msg_length :
				msg_length=int(msg_length)	                          #extract msg length to receive
				msg=conn.recv(msg_length).decode(FORMAT)              #set this as new buffer size to recieve actual message
				if msg == DISCONNECT_MESSAGE :
					connected=False

				msg_list=msg.split()
				print(f"[{address}] {msg_list}")



				if msg_list[0] == "CREATE_USER" :                    #command received= ['CREATE_USER', 'name', 'username', 'password']

					if(len(msg_list) != 4 ):
						msg="Error : Please provide proper args"
						self.send(msg,conn)

					else :

						new_user = user(msg_list[1],msg_list[2],msg_list[3],address[0],address[1])  #creating user object by calling its constuctor
						self.user_dict[msg_list[2]] = new_user                                      #adding user to server's list
						print("checking new user ",new_user.getIpPort())
						msg="user created succesfully"
						self.send(msg,conn)

				elif msg_list[0] =="LOGIN" :                       #command received= ['LOGIN','username','password']

					if(len(msg_list) != 3 ):
						# print()
						msg="Error : Please provide proper args"
						self.send(msg,conn)
					else :

						
						username = msg_list[1]
						password = msg_list[2]

						try :

							curr_user=self.user_dict[username]         #adding user to server's user list
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
						
								
				elif msg_list[0] == "SEND" :                     #command received= ['SEND','username','msg']
					print("Please send the message")              #or ['SEND', 'username', 'filename','file']


				elif msg_list[0] == "JOIN" :                     #command received= ['JOIN','username','groupname']
					print("Please JOIN the group")
					if len(msg_list) != 3 :
						msg="False"
						self.send(msg,conn)
					else :
						if msg_list[2] not in group_dict:
							self.create_group(msg_list[2],msg_list[1],conn)
						else :
							self.group_dict[msg_list[2]].add_member(msg_list[1])    #add user to group object's list
							self.user_dict[msg_list[1]].joinGroup(msg_list[2])      #add groupname to user class' grouplist
							msg="True"
							self.send(msg,conn)

				elif msg_list[0] == "CREATE" :                  #command received= ['CREATE','username''groupname']  
					if len(msg_list) != 3 :
						msg="False"
						self.send(msg,conn)
					else :
						self.create_group(msg_list[2],msg_list[1],conn)

					
				elif msg_list[0] == "LIST" :                     #command received=['LIST']
					groups= list(self.group_dict.keys())
					print("groups ",groups)
					if len(groups) == 0:
						msg = "NO GROUPS"
					else :
						msg=' '.join(groups)
					self.send(msg,conn)

		conn.close()	                                         #closing the connection with a client

	def create_group(self,grp,user_id,conn):
		if grp in self.group_dict.keys() :
			msg="False"
			self.send(msg,conn)
		else :
			self.group_dict[grp]=Group(grp)                  #put newly created group object in server's group dictionary
			self.group_dict[grp].add_member(user_id)         #add user to group object's list
			self.user_dict[user_id].joinGroup(grp)			 #add groupname to user class' grouplist
			msg="True"
			self.send(msg,conn)

						
	#Function to send message from server to client on port->contained in "connection" variable				
	def send(self,msg,connection) :
		message = msg.encode(FORMAT)                     #encode msg in utf-8
		msg_length = len(message)                        #extract length of msg
		send_length = str(msg_length).encode(FORMAT)     #encode length to send before sending actual msg
		send_length += b' ' * (HEADER -len(send_length)) #pad it to fit the initial buffer size=HEADER (64B)
		connection.send(send_length)                     #send length
		connection.send(message)						 #send message

    	
    	
   

print("[STARTING] server is starting .... ")
server=Server(SERVER,PORT)                               #creating server object and initializing its ip and port
server.server_start()



