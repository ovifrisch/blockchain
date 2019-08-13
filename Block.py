import hashlib
import json
from Transaction import Transaction
import time

class Block:
	"""
	A block (chain[i]) in the Blockchain

	Parameters
	----------
	timestamp : float
		- The time that the block was added to the chain
	transactions : List(Transaction)
		- The transactions contained within this block
	prev_hash : String
		- The hash of the previous block in the chain
	"""
	def __init__(self, timestamp=None, transactions=None, prev_hash=""):
		self.timestamp = timestamp
		self.transactions = transactions
		self.prev_hash = prev_hash

		# used to change the x in the x=>y of the hash function while mining
		self.nonce = 0
		self.hash = self.calculate_hash()


	"""
	Return
	------
	hash_ : String
		- hash of this Block
	"""
	def calculate_hash(self):
		# represent the transactions array as a string
		json_txs = json.dumps([x.__dict__ for x in self.transactions])
		hash_ = hashlib.sha256((self.prev_hash + str(self.timestamp) + json_txs + str(self.nonce)).encode('utf-8')).hexdigest()
		return hash_

	"""
	Mine this block. This means keep recalculating the hash (using changing nonce and timestamp)
	until it matches the pattern defined by the difficulty parameter. This function is the
	"Proof of Work" for when a miner wants to add a block to the chain.

	Parameters
	----------
	difficulty : Integer
		- the # of zeros required for the prefix of the hashs
	"""
	def mine_block(self, difficulty):
		while (self.hash[:difficulty] != "0" * difficulty):
			self.nonce += 1
			# recompute the time so that the timestamp is up to date
			self.timestamp = time.time()
			self.hash = self.calculate_hash()
		print("Block mined: {0}".format(self.hash))


	"""
	Verify if this block has valid transactions
	Why can't we just check if the hash of the block is the same? Beacuse
	the attacker could have modified something and then recomputed this hash
	based on that modification.

	Checking that each transaction in the block is valid will catch these
	modifications because of the public-private key cryptography used to
	create the transaction

	Return
	------
	: Boolean
		- True if valid, False otherwise
	"""
	def has_valid_transactions(self):
		for transactions in self.transactions:
			if (not transactions.is_valid()):
				return False
		return True
