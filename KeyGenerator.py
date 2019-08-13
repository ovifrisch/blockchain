from Crypto.PublicKey import RSA
import binascii


class KeyGenerator:
	"""
	Generator for public and private keys
	"""
	def __init__(self):
		pass

	"""
	Generate a random public-private key pair

	Return
	------
	keypair : Tuple(2)
		- The private and public keys
	"""
	def generate(self):
		sk = RSA.generate(1024)
		pk = binascii.hexlify(sk.publickey().exportKey(format='DER')).decode('ascii')
		keypair = (sk, pk)
		return keypair
