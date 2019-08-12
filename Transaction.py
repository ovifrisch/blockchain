import time
import hashlib
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import binascii

class Transaction:
	def __init__(self, from_address, to_address, amount):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.time()
		self.signature = None

	def calculate_hash(self):
		return SHA.new((self.from_address + self.to_address + str(self.amount) + str(self.timestamp)).encode('utf-8'))

	# encrypt the transaction
	def sign(self, secret_key):
		"""
		encrypt the message using the private key
		such that it can be decrypted using the public key
		"""
		signer = PKCS1_v1_5.new(secret_key)
		h = self.calculate_hash()
		self.signature = binascii.hexlify(signer.sign(h)).decode('ascii')

	def verify(self):
		public_key = RSA.importKey(binascii.unhexlify(self.from_address))
		verifier = PKCS1_v1_5.new(public_key)
		h = self.calculate_hash()
		return verifier.verify(h, binascii.unhexlify(self.signature))


	# decrypt the encyption using the from_address (public key)
	# and test if it is equal to self.calculate_hash
	def is_valid(self):
		if (not self.from_address):
			return True

		if (self.signature is None):
			return False

		if (self.verify()):
			return True
		else:
			return False



