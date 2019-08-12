from Block import Block
import time
from Transaction import Transaction

class Blockchain:
	def __init__(self):
		self.chain = [self.create_genesis_block()]
		self.difficulty = 2
		self.pending_transactions = []
		self.mining_reward = 100
		self.num_blocks = 1
		self.num_transactions = 0

	def create_genesis_block(self):
		return Block(time.time(), [])

	def get_latest_block(self):
		return self.chain[-1]

	# some transactions that have been approved may actually lead to
	# a negative balance because of other pending transactions not
	# yet taken into account. Here we invalidate those transactions
	# before committing them to the chain

	# any transaction that goes negative will not be included
	def filter_pending_transactions(self):

		# public key to balance
		h = {}

		# filtered transactions
		res = []
		for tx in self.pending_transactions:
			if (tx.to_address not in h):
				h[tx.to_address] = self.get_balance_of_address(tx.to_address)

			if (tx.from_address is None):
				h[tx.to_address] += tx.amount
				res.append(tx)
				continue

			if (tx.from_address not in h):
				h[tx.from_address] = self.get_balance_of_address(tx.from_address)

			if (h[tx.from_address] - tx.amount < 0):
				continue
			else:
				h[tx.to_address] += tx.amount
				h[tx.from_address] -= tx.amount

			res.append(tx)
		return res


	def mine_pending_transactions(self, mining_reward_address):
		if (not self.pending_transactions):
			return
		reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
		self.pending_transactions.append(reward_tx)
		self.pending_transactions = self.filter_pending_transactions()
		block = Block(time.time(), self.pending_transactions, self.get_latest_block().hash)
		block.mine_block(self.difficulty)

		## proof or work ##
		self.chain.append(block)
		self.num_blocks += 1
		self.num_transactions += len(self.pending_transactions)

		self.pending_transactions = []

	def add_transaction(self, transaction):
		if (not transaction.to_address):
			print("Transaction must include to address")
			return

		if (not transaction.is_valid()):
			print("Invalid Transaction")
			return

		if (transaction.amount <= 0):
			print("Transaction amount must be positive")
			return

		if (transaction.from_address is not None):
			bal = self.get_balance_of_address(transaction.from_address)
			if (bal - transaction.amount < 0):
				print("Insufficient funds to make this transaction")
				return

		print("Transaction successfully added to pending transactions")
		self.pending_transactions.append(transaction)


	def get_balance_of_address(self, addr):
		bal = 0
		for block in self.chain:
			for transaction in block.transactions:
				if (transaction.from_address is not None and transaction.from_address == addr):
					bal -= transaction.amount

				if (transaction.to_address == addr):
					bal += transaction.amount
		return bal


	def get_all_transactions_for_wallet(self, addr):
		txs = []
		for block in self.chain:
			for tx in block.transactions:
				if (tx.from_address == addr or tx.to_address == addr):
					txs.append(tx)
		return txs

	def is_chain_valid(self):
		# starting from the end of the block
		for i in range(len(self.chain) - 1, 0, -1):
			blk = self.chain[i]
			# first check if the block's hash is really the hash
			if (blk.calculate_hash() != blk.hash):
				return False

			# the above test could pass even if someone tampered w the blk
			"""
			ex: someone changes anything on the block and then
			recomputes the hash and sets the hash equal to this.
			cont... if the change was made somwehere in the transactions
			array, then we can detect it by decrypting the signature w the pk
			and comparing to the recalculated hash of the transaction.
			if someone tampered with the amount, then they won't be equal.
			maybe you think that the attacker could also tamper with the
			signature so that its decryption would be equal to the new
			hash. But he would need the private key to make this work. If he
			doesnt have sk, he is left with guess and check, and if the signature
			is long enough this quickly becomes infeasible.

			SO, let's now check if someone tampered with any of the transactions


			"""
			if (not blk.has_valid_transactions()):
				return False

			# now check if someone deleted a block by comparing the prevHash
			# to the hash of the previous element on the blockchain

			if (blk.prev_hash != self.chain[i-1].calculate_hash()):
				return False
		return True





