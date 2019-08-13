import time
import hashlib
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import binascii

class Transaction:
	"""
	Transaction between two public keys

	Parameters
	----------
	from_address : String
		- Public key of sender
	to_address : String
		- Public key of receiver
	amount : Float
		- amount to be transfered
	"""
	def __init__(self, from_address, to_address, amount):
		self.from_address = from_address
		self.to_address = to_address
		self.amount = amount
		self.timestamp = time.time()

		# Encryption of the hash of this transaction
		self.signature = None

	"""
	Return
	------
	hash - Crypto.Hash.SHA.SHA1Hash
		An object that contains the hash of this transaction (calculated using unique combination of transaction params)
	"""
	def calculate_hash(self):
		hash_ = SHA.new((self.from_address + self.to_address + str(self.amount) + str(self.timestamp)).encode('utf-8'))
		return hash_

	"""
	This function is called by the sender of a transaction to sign (encrypt) it and store the encryption
	in self.signature

	Parameters
	----------
	sk : Crypto.PublicKey.RSA
		- Secret key corresponding to the Public Key (from_address) of this transaction
	"""
	def sign(self, sk):
		# sign using secret key and hash
		signer = PKCS1_v1_5.new(sk)
		hash_ = self.calculate_hash()
		self.signature = binascii.hexlify(signer.sign(hash_)).decode('ascii')

	"""
	This function is used to verify that the transaction has not been altered since it was
	signed. It does so by using the public key and the recomputed hash of this object

	Return
	------
	is_valid : Boolean
		- True if transaction has not been altered, False otherwise
	"""
	def verify(self):
		# create the public key object from the public key string
		public_key = RSA.importKey(binascii.unhexlify(self.from_address))
		verifier = PKCS1_v1_5.new(public_key)

		# recompute hash
		h = self.calculate_hash()

		is_valid = verifier.verify(h, binascii.unhexlify(self.signature))
		return is_valid


	# decrypt the encyption using the from_address (public key)
	# and test if it is equal to self.calculate_hash

	"""
	Check if this transaction is valid
	"""
	def is_valid(self):

		# No from_address means this is a miner's reward transaction
		if (not self.from_address):
			return True

		# Needs to be signed
		if (self.signature is None):
			return False

		# finally, has it been altered?
		return self.verify()



