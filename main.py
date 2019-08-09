from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Blockchain import Blockchain
from Transaction import Transaction

sk = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
	backend=default_backend()
)

pk = sk.public_key()
pem = pk.public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
print(pem)