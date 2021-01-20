import random
from des import DesKey

# from Crypto.Cipher import DES3
# from Crypto.Util.Padding import pad

#pip install des


class Diffie_Hellman:
	roll_no=2020202019
	mod_pub=3343036042667233507069333705267738066150537335329373445649
	exp_pub=150449272774067166433654322282031043481528926326708716556
	def __init__(self):
		
		pri_key=random.getrandbits(192)
		
		pri_key+=self.roll_no
		self.private_key=pri_key

	def create_intermediate_key(self):
		intermediate_key=pow(self.exp_pub,self.private_key,self.mod_pub)
		return intermediate_key

	def get_shared_key(self,intermediate_key):
		
		intermediate_key=int(intermediate_key)
		shared_key=pow(intermediate_key,self.private_key,self.mod_pub)
		return shared_key





class DES:
	def __init__(self,key):
		
		key=key.to_bytes(24, byteorder='big')
		self.key=key
		self.create_cipher()

	def create_cipher(self):

		# try:
		# 	key2 = DES3.adjust_key_parity(self.key)

		# except ValueError:
		# 	pass
		# self.cipher = DES3.new(key1, DES3.MODE_CFB)
		# print(self.key)
		# key2=pad(self.key,24)
		# print(key2)
		assert(len(self.key) == 24)
		self.key1=DesKey(self.key)
		# print(self.key1.is_triple())

	def encryption(self,data):
		data=data.encode()
		cipher_text=self.key1.encrypt(data, padding=True)
		return cipher_text

	def decryption(self,data):
		
		plain_text=self.key1.decrypt(data, padding=True)
		return plain_text.decode()



