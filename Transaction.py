import time
import hashlib
import cryptography

class Transaction:
	def __init__(self, from_address, to_address, amount):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.time()

	def calculate_hash(self):
		return hashlib.sha256((from_address + to_address + str(amount) + str(timestamp)).encode('utf-8')).hexdigest()

	# encrypt the transaction
	def encrypt(self, private_key, public_key):
		"""
		encrypt the message using the private key
		such that it can be decrypted using the public key
		"""
		encryption = 0 # implement??
		self.encryption = encryption


	def is_valid(self):
		if (not self.from_address):
			return True

