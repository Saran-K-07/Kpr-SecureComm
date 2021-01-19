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

        print(f"[*] Host: {self.CLIENT_IP} | Port: {self.PORT}")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connectToServer(self):
        try:
            self.client.connect((self.SERVER_IP, self.PORT))

        except socket.error as e:
            print(str(e))
            sys.exit()

    def operate(self):

    	quit=False
    	while quit == False :
    		print("Lets start")
    		my_input=input()
    		self.send(my_input)

    		

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
		
	

