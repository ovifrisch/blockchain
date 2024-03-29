from Blockchain import Blockchain
from Transaction import Transaction
from KeyGenerator import KeyGenerator
from Wallet import Wallet
import random

if __name__ == "__main__":
	ovi_coin = Blockchain(difficulty=2, mining_reward=100)
	keygen = KeyGenerator()
	names = ["Miner", "Ovi", "Bob", "Alice", "Peter", "Collin", "Mark", "Daniel", "Alex", "Jane", "Jill"]
	threads = []

	# create 11 wallets
	wallets = []
	for i in range(11):
		sk, pk = keygen.generate()
		wallets.append(Wallet(names[i], pk, sk))

	# have a designated miner
	miner = wallets[0]
	wallets = wallets[1:]

	# everybody starts with $100
	for i in range(10):
		tx = Transaction(None, wallets[i].pk, 100)
		ovi_coin.add_transaction(tx)
	threads.append(ovi_coin.mine_pending_transactions(miner.pk))


	# randomly execute 100 transactions between the wallets
	# and mine every 10
	for i in range(1, 101):

	# 	# generate 2 random idxs that aren't equal
		s = r = 0
		while (s == r):
			s = random.randint(0, 9)
			r = random.randint(0, 9)

	# 	# generate a random amount between 1 and 100
		amt = random.randint(1, 100)

	# 	# create the transaction
		tx = Transaction(wallets[s].pk, wallets[r].pk, amt)
		tx.sign(wallets[s].sk)
		ovi_coin.add_transaction(tx)

	# 	# mine every 5
		if (i % 5 == 0):
			threads.append(ovi_coin.mine_pending_transactions(miner.pk))
	threads.append(ovi_coin.mine_pending_transactions(miner.pk))
	
	for thread in threads:
		if (thread):
			thread.join()

	for wallet in [miner] + wallets:
		wallet.show(ovi_coin)



