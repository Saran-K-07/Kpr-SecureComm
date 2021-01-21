import socket
import threading
from user_client import user_client
from security import Diffie_Hellman,DES
import sys

PORT = 5051 
HEADER = 64
FORMAT = "utf-8"
# SERVER = socket.gethostbyname(socket.gethostname())

SERVER = "127.0.0.2"
#ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE="!DISCONNECT"

class Client:
    def __init__(self, server_ip, port, client_ip):
        self.SERVER_IP = server_ip                              #server's ip to connect to
        self.PORT = port										#server's port to connect to
        self.CLIENT_IP = client_ip    							#client's own ip
        self.isLoggedIn=False  									#active status of client
        self.ADDR=(self.SERVER_IP,self.PORT)  							#tuple of server ip and server address
        print(f"[*] Host: {self.CLIENT_IP} | Port: {self.PORT}")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #socket object on client side
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.current_userid=""
        thread=threading.Thread(target=self.listen_client)
        thread.start()

    def connectToServer(self):
        try:
            self.client.connect((self.ADDR))                      #establish connection with server on address ADDR=SERVER_IP,SERVER_PORT

        except socket.error as e:
            print(str(e))
            sys.exit()
        self.shared_key_server()
        

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
    			self.encrypted_send(my_input,self.user_key_pair.server_key)
    			self.create_user(my_input_list)


    		elif(my_input_list[0] == "CREATE")	:
    			self.create_group(my_input_list) 
    		elif(my_input_list[0] == "SEND")	:
    			self.send_message(my_input_list) 
    		elif(my_input_list[0] == "LOGIN")	:
    			self.encrypted_send(my_input,self.user_key_pair.server_key)
    			self.login_user(my_input_list) 
    		elif(my_input_list[0] == "JOIN")	:
    			self.join_group(my_input_list) 
    		elif(my_input_list[0] == "LIST") :
    			self.encrypted_send(my_input,self.user_key_pair.server_key) 	
    			self.list_group(my_input_list) 
    		elif(my_input_list[0] == "SEND_TO_GROUP")	:
    			self.send_to_group(my_input_list) 





    		
	#function to handle message received from others over a socket
    def recieve_message(self,cli=None):
        if cli==None:
            cli=self.client
            msg=""
            msg_length=cli.recv(HEADER).decode(FORMAT)   #get length of  msg to receive by using initial buffer size of header=64B
            if msg_length :
                msg_length=int(msg_length)	                    #convert length to int as it was received in utf-8 format
                msg=cli.recv(msg_length).decode(FORMAT)	 #reset buffer size to received msg length size and receive msg

        return msg


    def recieve_message_decrypt(self,key,cli=None):
        if cli==None:
            cli=self.client
            msg=""
            msg_length=cli.recv(HEADER).decode(FORMAT)   #get length of  msg to receive by using initial buffer size of header=64B
            if msg_length :
                msg_length=int(msg_length)                      #convert length to int as it was received in utf-8 format
                msg=cli.recv(msg_length)  #reset buffer size to received msg length size and receive msg
                msg=DES(key).decryption(msg)
        return msg


    def create_user(self,command_list):

    	msg=self.recieve_message_decrypt(self.user_key_pair.server_key)
    	print(msg)	
    	print("\n")

    def login_user(self,command_list):
    	msg=self.recieve_message_decrypt(self.user_key_pair.server_key)
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
    		self.encrypted_send(send_msg,self.user_key_pair.server_key)
    		msg=self.recieve_message_decrypt(self.user_key_pair.server_key)
    		
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
            self.encrypted_send(send_msg,self.user_key_pair.server_key)    		
            msg=self.recieve_message_decrypt(self.user_key_pair.server_key)

            if(msg=="True") :

                print(f"{self.current_userid} joined group {command_list[1]} succesfully ")

            else :
                print("Invalid command")

        print("\n")

    def send_message(self,command_list):
        #check if we have to send file or not 
        #get the user info from server
        #create client as a sever
        #send message from p2p
        #if message is type of file then create a function to send file
        send_msg=command_list[0]+" "+ self.current_userid+" "+ command_list[1]

        self.encrypted_send(send_msg,self.user_key_pair.server_key)
        msg=self.recieve_message_decrypt(self.user_key_pair.server_key)

        # print(msg)
        ip=msg.split(" ")[0]
        port=int(msg.split(" ")[1])

        thread1=threading.Thread(target=self.send_message_data,args=(ip,port,command_list))
        thread1.start()

    def send_message_data(self,ip,port,command_list):
        cli_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:                       
            addr=(ip,port)            
            print(addr)
            cli_server.connect(addr)                      #establish connection with server on address ADDR=SERVER_IP,SERVER_PORT
            
        except socket.error as e:
            print(str(e))
            sys.exit()
        
        self.send(self.user_key_pair.imd_key,cli_server)
        sk=self.recieve_message(cli_server)
        sk=Diffie_Hellman(user_key_pair.private_key).create_shared_key(sk)
        print(f"Key:{sk}")
        self.encrypted_send(command_list[2],sk,cli_server)
        




    	

    def list_group(self,command_list):
    	print(" group list ")
    	msg=self.recieve_message_decrypt(self.user_key_pair.server_key)
    	print(msg)

    def send_to_group(self,command_list):

        #multiple groups can be there so extract the group names
        #for each group extract the each member info (user id ,ip ,port )
        #for each user  in each group use send message to send message

    	print(command_list)	

    def clientAsserver(self) :
        pass

    	
    def send(self,msg,cli=None) :
        if cli==None:
            cli=self.client
        msg=str(msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER -len(send_length))
        cli.send(send_length)
        cli.send(message)
		
    def shared_key_server(self):
        self.user_key_pair=user_client(self.current_userid)
        self.send(self.user_key_pair.imd_key)
        sk=self.recieve_message()
        sk=Diffie_Hellman(self.user_key_pair.private_key).create_shared_key(sk)
        print(f"Key:{sk}")
        self.user_key_pair.set_server_key(sk)


    def encrypted_send(self,msg,key,cli=None):
        if cli==None:
            cli=self.client
        message=DES(key).encryption(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER -len(send_length))        
        cli.send(send_length)
        cli.send(message)       


    def listen_client(self):
        try:
            CLI_ADDR=self.client.getsockname()
            cli_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            cli_server.bind(CLI_ADDR)            
        except socket.error as e:
            print(str(e))
        print("//////////////////SERVER STARTED///////////")
        cli_server.listen(5)
        while True : 

            connection,address=cli_server.accept()
            print("/////////")
            thread1=threading.Thread(target=self.handle_client,args=(connection,address))
            thread1.start()
            thread1.join()

    def handle_client(self,conn,address):
        msg=self.recieve_message(conn)            
        sk=Diffie_Hellman(self.private_key).create_shared_key(msg)
        print(f"Key:{sk}")        
        self.send(self.imd_key,conn)
        msg=self.recieve_message_decrypt(sk,conn)
        print(f"->{msg}")


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
		
	
