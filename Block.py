import hashlib
import json
from Transaction import Transaction

class Block:

	def __init__(self, timestamp, transactions, prev_hash=""):
		self.timestamp = timestamp
		self.transactions = transactions
		self.prev_hash = prev_hash
		self.nonce = 0
		self.hash = self.calculcate_hash()


	def calculate_hash(self):
		return hashlib.sha256((self.previous_hash + str(self.timestamp) + json.dumps(transactions) + str(this.nonce)).econde('utf-8')).hexdigest()



	def mine_block(self, difficulty):

		while (self.hash[:difficulty] != "0" * difficulty):
			self.nonce += 1
			self.calculate_hash()

		print("Block mined: {0}".format(self.hash))
