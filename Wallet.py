
class Wallet:
	def __init__(self, first_name, pk, sk):
		self.first_name = first_name
		self.pk = pk
		self.sk = sk

	def get_balance(self, chain):
		return chain.get_balance_of_address(self.pk)

	def get_all_transactions(self, chain):
		return chain.get_all_transactions_for_wallet(self.pk)

	def get_incoming_transactions(self, chain):
		return [x for x in chain.get_all_transactions_for_wallet(self.pk) if x.to_address == self.pk]

	def get_outgoing_transactions(self, chain):
		return [x for x in chain.get_all_transactions_for_wallet(self.pk) if x.from_address == self.sk]

	def show(self, chain):
		print("Name: " + self.first_name + " Balance: " + str(self.get_balance(chain)))