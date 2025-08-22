import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Block mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, time.time(), ["Genesis Block"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address):
        # reward transaction
        self.pending_transactions.append(
            {"from": "System", "to": miner_address, "amount": self.mining_reward}
        )

        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)

        self.chain.append(block)
        self.pending_transactions = []  # reset transactions

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount
        })

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(json.dumps({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }, indent=4))
            print("-" * 40)


# --- CLI Demo ---
if __name__ == "__main__":
    my_coin = Blockchain()

    while True:
        print("\n=== Simple Blockchain System by Jhasim ===")
        print("1. Add transaction")
        print("2. Mine block")
        print("3. Show blockchain")
        print("4. Validate blockchain")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            sender = input("From: ")
            recipient = input("To: ")
            amount = input("Amount: ")
            my_coin.add_transaction(sender, recipient, amount)
            print("Transaction added!")

        elif choice == "2":
            miner = input("Enter miner address: ")
            my_coin.mine_pending_transactions(miner)

        elif choice == "3":
            my_coin.print_chain()

        elif choice == "4":
            print("Blockchain valid?", my_coin.is_chain_valid())

        elif choice == "5":
            break

        else:
            print("Invalid choice, try again.")
