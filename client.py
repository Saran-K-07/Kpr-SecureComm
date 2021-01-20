import socket
import threading

PORT = 5050 
HEADER = 64
FORMAT = "utf-8"
# SERVER = socket.gethostbyname(socket.gethostname())

SERVER = "127.0.0.2"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE="!DISCONNECT"

class Client:
    def __init__(self, server_ip, port, client_ip):
        self.SERVER_IP = server_ip
        self.PORT = port
        self.CLIENT_IP = client_ip    
        self.isLoggedIn=False  

        print(f"[*] Host: {self.CLIENT_IP} | Port: {self.PORT}")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_userid=""


    def connectToServer(self):
        try:
            self.client.connect((self.SERVER_IP, self.PORT))

        except socket.error as e:
            print(str(e))
            sys.exit()

    def operate(self):

    	quit=False
    	while quit == False :
    		print("Please choose from one of the following commands")
    		print("CREATE_USER <NAME> <USER_NAME> <PASSWORD>")
    		print("LOGIN <USER_NAME> <PASSWORD>")
    		print("JOIN <GROUP_NAME> ")
    		print("CREATE <GROUP_NAME> ")
    		print("LIST")
    		print("SEND <USER_NAME> <MESSAGE>")
    		print("SEND_TO_GROUP <GROUP_NAME> <MESSAGE>")
    		print("SEND FILE <USER_NAME> <FILENAME>")
    		print("SEND_TO_GROUP FILE <GROUP_NAME> <FILENAME>")
    		print()


    		my_input=input()
    		my_input_list=my_input.split()
    		print("my_input_list " ,my_input_list)
    		

    		if(my_input_list[0] == "CREATE_USER") :
    			self.send(my_input)
    			self.create_user(my_input_list)


    		elif(my_input_list[0] == "CREATE")	:
    			self.create_group(my_input_list) 
    		elif(my_input_list[0] == "SEND")	:
    			self.send_message(my_input_list) 
    		elif(my_input_list[0] == "LOGIN")	:
    			self.send(my_input)
    			self.login_user(my_input_list) 
    		elif(my_input_list[0] == "JOIN")	:
    			self.join_group(my_input_list) 
    		elif(my_input_list[0] == "LIST") :
    			self.send(my_input) 	
    			self.list_group(my_input_list) 
    		elif(my_input_list[0] == "SEND_TO_GROUP")	:
    			self.send_to_group(my_input_list) 





    		

    def recieve_message(self ):
    	msg=""
    	msg_length=self.client.recv(HEADER).decode(FORMAT)
    	if msg_length :
    		msg_length=int(msg_length)	
    		msg=self.client.recv(msg_length).decode(FORMAT)	
			
    	return msg
		


    def create_user(self,command_list):

    	msg=self.recieve_message()
    	print(msg)	
    	print("\n")

    def login_user(self,command_list):
    	msg=self.recieve_message()
    	print(msg)
    	if(msg=="True") :
    		self.current_userid = command_list[1]
    		self.isLoggedIn=True
    		print(f"{command_list[1]} logged in succesfully ")
    	else :
    		print("Invalid Credentials")
    	print("\n")

    def create_group(self,command_list):

    	if self.isLoggedIn == False :
    		print("\n")
    		print("Please Login First")
    		print("\n")
    	else :
    		send_msg=command_list[0]+" "+ self.current_userid+" "+command_list[1]
    		self.send(send_msg)
    		msg=self.recieve_message()
    		
    		if(msg=="True") :
    			
    			print(f"{command_list[1]} group created succesfully ")
    		
    		else :
    			print("Group exists! Please use JOIN command to join the group")
    	
    		print("\n")
    	
    		
    		    	

    def join_group(self,command_list):
    	if self.isLoggedIn == False :
    		print("\n")
    		print("Please Login First")
    		print("\n")
    	else :
    		send_msg=command_list[0]+" "+ self.current_userid+" "+command_list[1]
    		self.send(send_msg)
    		msg=self.recieve_message()
    		
    		if(msg=="True") :
    			
    			print(f"{self.current_userid} joined group {command_list[1]} succesfully ")
    		
    		else :
    			print("Invalid command")
    	
    		print("\n")

    def send_message(self,command_list):
    	print(command_list)

    def list_group(self,command_list):
    	print(" group list ")
    	msg=self.recieve_message()
    	print(msg)

    def send_to_group(self,command_list):
    	print(command_list)	
    	
    def send(self,msg) :
    	message = msg.encode(FORMAT)
    	msg_length = len(message)
    	send_length = str(msg_length).encode(FORMAT)
    	send_length += b' ' * (HEADER -len(send_length))
    	self.client.send(send_length)
    	self.client.send(message)
		
		
   


client =Client(SERVER,PORT,"127.0.0.1")
client.connectToServer()
client.operate()
# client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client.connect(ADDR)




# out= 1
# while out :
# 	txt=input()
	
# 	if(txt== "quit" ):
# 		send(DISCONNECT_MESSAGE)
# 		out=0
# 	else :
# 		send(txt)
		
	

