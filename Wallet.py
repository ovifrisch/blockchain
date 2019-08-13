
class Wallet:
	"""
	Wallet for an Individual

	Parameters
	----------
	first_name : String
		- Name of the individual
	pk : String
		- Public Key for the individual
	sk : Crypto.PublicKey.RSA
		- Object containing Private Key for the individual
	"""
	def __init__(self, first_name, pk, sk):
		self.first_name = first_name
		self.pk = pk
		self.sk = sk

	"""
	Parameters
	----------
	chain : Blockchain
		The chain we are getting this wallet's balance from

	Return
	------
	balance : Float
		The balance for this wallet
	"""
	def get_balance(self, chain):
		balance = chain.get_balance_of_address(self.pk)
		return balance


	"""
	Parameters
	---------
	chain : Blockchain
		The chain we are getting this wallet's balance from

	Return
	------
	txs : List(Transaction)
		All transactions for this wallet
	"""
	def get_all_transactions(self, chain):
		txs = chain.get_all_transactions_for_wallet(self.pk)
		return txs

	"""
	Parameters
	---------
	chain : Blockchain
		The chain we are getting this wallet's balance from

	Return
	------
	txs : List(Transaction)
		All incoming transactions for this wallet
	"""
	def get_incoming_transactions(self, chain):
		txs = [x for x in chain.get_all_transactions_for_wallet(self.pk) if x.to_address == self.pk]
		return txs

	"""
	Parameters
	---------
	chain : Blockchain
		The chain we are getting this wallet's balance from

	Return
	------
	txs : List(Transaction)
		All outgoing transactions for this wallet
	"""
	def get_outgoing_transactions(self, chain):
		txs = [x for x in chain.get_all_transactions_for_wallet(self.pk) if x.from_address == self.sk]
		return txs

	"""
	Parameters
	---------
	chain : Blockchain
		The chain we are getting this wallet's balance from

	Prints the name and balance for this wallet
	"""
	def show(self, chain):
		print("Name: " + self.first_name + " Balance: " + str(self.get_balance(chain)))

