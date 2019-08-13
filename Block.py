import hashlib
import json
from Transaction import Transaction

class Block:

	def __init__(self, timestamp=None, transactions=None, prev_hash=""):
		self.timestamp = timestamp
		self.transactions = transactions
		self.prev_hash = prev_hash
		self.nonce = 0
		self.hash = self.calculate_hash()


	def calculate_hash(self):
		return hashlib.sha256((self.prev_hash + str(self.timestamp) + json.dumps([x.__dict__ for x in self.transactions]) + str(self.nonce)).encode('utf-8')).hexdigest()

	def mine_block(self, difficulty):
		while (self.hash[:difficulty] != "0" * difficulty):
			self.nonce += 1
			self.hash = self.calculate_hash()
		print("Block mined: {0}".format(self.hash))


	def has_valid_transactions(self):
		for transactions in self.transactions:
			if (not transactions.is_valid()):
				return False
		return True
