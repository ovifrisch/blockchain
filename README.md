# A Blockchain Implementation in Python

## Usage: 

Dependencies:
```python
pip install pycrypto
```

Then:
```python
from Blockchain import Blockchain
from Transaction import Transaction
from KeyGenerator import KeyGenerator
from Wallet import Wallet
```

Create Blockchain:

```python
my_coin = Blockchain(mining_difficulty=2, mining_reward=100)
```

Create some public and secret key pairs:
```python
key_gen = KeyGenerator()
sk1, pk1 = key_gen.generate()
sk2, pk2 = key_gen.generate()
```

Create some wallets:
```python
bob = Wallet("Bob", pk1, sk1)
alice = Wallet("Alice", pk2, sk2)
```

Add and sign a transaction:
```python
tx1 = Transaction(from_address=pk1, to_address=pk2, amount=300)
tx1.sign(sk1)
```

Mine pending transactions
```python
my_coin.mine_pending_transactions(mining_reward_address=pk1)
```

Get a wallet's balance
```python
balance = bob.get_balance(my_coin)
```

Get a wallet's transactions
```python
txs = bob.get_all_transactions(my_coin)
```

Check if a chain is valid
```python
valid = my_coin.is_valid()
```
