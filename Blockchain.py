from Block import Block
import time
from Transaction import Transaction

class Blockchain:
	def __init__(self):
		self.chain = [create_genesis_block()]
		self.difficulty = 2
		self.pending_transactions = []
		self.mining_reward = 100

	def create_genesis_block(self):
		return Block(time.time(), [])

	def get_latest_block(self):
		return self.chain[-1]

	def mine_pending_transactions(self, mining_reward_address):
		block = Block(time.time(), self.pending_transactions, self.get_latest_block().hash)
		block.mine_block(self.difficulty)

		print("Block successfully mined!")

		self.chain.append(block)

		reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
		self.pending_transactions = [reward_tx]

	def add_transaction(self, transaction):
		if (not transaction.from_address or not transaction.to_address):
			raise Exception("Transaction must include from and to address")

		if (not transaction.is_valid()):
			raise Exception("Invalid Transaction")

		if (transaction.amount <= 0):
			raise Exception("Transaction amount must be positive")

		self.pending_transactions.append(transaction)


	def get_balance_of_address(addr):
		bal = 0
		for block in self.chain:
			for transaction in block.transactions:
				if (transaction.from_address == addr):
					bal -= transaction.amount

				if (transaction.to_address == addr):
					bal += transaction.amount
		return bal


	def get_all_transactions_for_wallet(addr):
		txs = []
		for block in self.chain:
			for tx in block.transactions:
				if (tx.from_address == addr or tx.to_address == addr):
					txs.append(tx)
		return txs

	def is_chain_valid(self):
		






