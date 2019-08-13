from Block import Block
import time
from Transaction import Transaction
import threading

"""
Known vulnerabilities:

First and Last Blocks in chain can be removed without being detected
	- Possible fix: store the max size of the chain. If size is ever less, deletion
	detected. (Now what stops someone from also modifying size variable?)

Client can create transaction from a "None" public key without being detected
	- How else do you introduce coins in a chain if the chain is designed
	so that it never allows transactions that cause a negative balance in
	the wallet of the from_address?
"""

class Blockchain:
	"""
	Distributed Ledger of transactions

	Parameters
	----------
	difficulty : Integer
		- the # of zeros required for the prefix of the hashs
	mining_reward : Float
		- the amount of coins a miner gets for successfully adding a block to the chain

	"""
	def __init__(self, difficulty, mining_reward):
		self.difficulty = difficulty
		self.mining_reward = mining_reward

		# the cryptographically linked list of blocks
		self.chain = [self.create_genesis_block()]

		# transactions that have been added but not yet mined
		self.pending_transactions = []

		# the number of blocks in the chain
		self.num_blocks = 1

		# the number of mined transactions
		self.num_transactions = 0

		# a lock for preventing multiple blocks to be mined at the same time on a single machine
		self.lock = threading.Lock()

	"""
	Return
	------
	genesis_block : Block
		- the first block on the chain (needed for setting prev_hash param of subsequent blocks)
	"""
	def create_genesis_block(self):
		genesis_block = Block(time.time(), [])
		return genesis_block

	"""
	Return
	------
	latest_block : Block
		- the last block on the chain
	"""
	def get_latest_block(self):
		latest_block = self.chain[-1]
		return latest_block

	"""
	Filter transactions such that when they are added to the chain,
	no wallet will have a negative balance. This means that
	transactions causing a negative balance in the from_address
	are ignored. Since only 1 block is being mined at a time,
	we can be sure that no other blocks that have valid transactions
	within themselves will be added to the chain and possible make
	some of these transactions invalid. Locking mechanism prevents
	this from happening. (fixed issue)

	Parameters
	----------
	transactions : List(Transaction)
		- the unfiltered pending transactions array

	Return
	------
	filtered_transactions : List(Transaction)
		- the filtered penfing transactions array

	"""
	def filter_transactions(self, transactions):

		# hash mapping publicKeys to their balance
		h = {}

		# filtered transactions
		filtered_transactions = []

		for tx in transactions:

			# store to_address balance in hash if not there already
			if (tx.to_address not in h):
				h[tx.to_address] = self.get_balance_of_address(tx.to_address)

			# if from address is None, this transaction doesn't subtract an amount from any wallet, so don't filter
			if (tx.from_address is None):
				h[tx.to_address] += tx.amount
				filtered_transactions.append(tx)
				continue

			# store from_address in hash if not already there
			if (tx.from_address not in h):
				h[tx.from_address] = self.get_balance_of_address(tx.from_address)

			# if the transaction's amount leads to a  negative balance in the sender's wallet, filter
			if (h[tx.from_address] - tx.amount < 0):
				continue

			# otherwise, update the balance in the hash for both public keys
			else:
				h[tx.to_address] += tx.amount
				h[tx.from_address] -= tx.amount

			# if message has not been filtered, add it to the result
			filtered_transactions.append(tx)
		return filtered_transactions


	"""
	Private method to mine transaction
	**Read the public method with the same name first to understand this function**

	This method is the target of a thread spawned by the main process
	It uses a lock to ensure that only one instance of this function
	is executing at once.

	Creates a block to mine 

	Parameters
	----------
	mining_reward_address : String
		- The publicKey for which to send the mining reward
	transactions : List(transactions)
		- The transactions to add to the block to mine
	"""
	def __mine_pending_transactions(self, mining_reward_address, transactions):
		with self.lock:
			# don't create a block with 0 transactions
			if (not transactions):
				return

			# create the mining reward transaction and add it to transactions
			reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
			transactions.append(reward_tx)

			# make sure no transactions will cause a negaitve balance in a wallet
			transactions = self.filter_transactions(transactions)

			# create the block
			block = Block(time.time(), transactions, self.get_latest_block().hash)

			## mine the block and then add it to the chain ##

			block.mine_block(self.difficulty) # COMPUTATION HEAVY

			print("mined" + str(len(transactions)))
			self.chain.append(block)
			self.num_blocks += 1
			self.num_transactions += len(transactions)


	"""
	Public method to mine all pending transactions. We want to make sure that (1) we don't have to
	wait for a successfully mined block in order to add more transactions, (2) that only 1 block is
	being mined at a time, and (3) that we include only those transactions that exist at the
	time this method is called.

	To solve (1): I spawn a new thread for the mining process
	To solve (2): I use a lock on the mining process so that only 1 thread can mine at once.
	To solve (3): I create a copy of the pending_transactions member variable, then reset it.
	I call the thread with the copy. If the thread blocks, even though more transactions may
	be added, they are added to the member variable, not the copy.

	Parameters
	----------
	mining_reward_address : String
		- The publicKey for which to send the mining reward

	Return
	------
	miner : threading.Thread
		The thread spawned for the mining process
	"""
	def mine_pending_transactions(self, mining_reward_address):
		transactions = self.pending_transactions;
		self.pending_transactions = []
		miner = threading.Thread(group=None, target=self.__mine_pending_transactions, args=(mining_reward_address,transactions))
		miner.start()
		return miner


	"""
	Add a transaction to the pending_transactions

	Parameters
	----------
	transaction : Transaction
		- the transaction to add to pending_transactions
	"""
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

		print("Transaction successfully added to pending transactions")
		self.pending_transactions.append(transaction)


	"""
	Get the balance of the wallet with the publicKey "addr"

	Parameters
	----------
	addr : String
		- publicKey

	Return
	------
	balance : Float
		- the balance for this address
	"""
	def get_balance_of_address(self, addr):
		balance = 0
		for block in self.chain:
			for transaction in block.transactions:

				# subtract if sending $
				if (transaction.from_address == addr):
					balance -= transaction.amount

				# add if receiving $
				if (transaction.to_address == addr):
					balance += transaction.amount
		return balance


	"""
	Get all the transactions of wallet with the publicKey "addr"

	Parameters
	----------
	addr : String
		- publicKey


	Return
	------
	txs : List(Transaction)
		- the transactions for this address
	"""
	def get_all_transactions_for_wallet(self, addr):
		txs = []
		for block in self.chain:
			for tx in block.transactions:
				if (tx.from_address == addr or tx.to_address == addr):
					txs.append(tx)
		return txs


	"""
	Check whether the chain is valid

	Return
	------
	: Boolean
		- True if chain is valid, False otherwise
	"""
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





