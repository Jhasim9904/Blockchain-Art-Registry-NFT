# blockchain.py
import hashlib
import json
import datetime
import time
from typing import List, Dict

# --- Helpers ---
def sha256_hex(data) -> str:
    if not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# --- Block & Chain ---
class Block:
    def __init__(self, index: int, timestamp: str, transactions: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions  # list of dicts
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = ""  # set after mining

    def _payload(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

    def calculate_hash(self) -> str:
        return sha256_hex(self._payload())

    def mine(self, difficulty: int):
        target = "0" * difficulty
        while True:
            candidate = self.calculate_hash()
            if candidate.startswith(target):
                self.hash = candidate
                return
            self.nonce += 1

class ArtChain:
    """
    Digital Art Ownership chain.
    transactions are dicts with keys:
      - action: "GENESIS" | "MINT" | "TRANSFER"
      - asset_hash: sha256 of file bytes
      - filename: stored filename on server (uploads/<hash>.<ext>)
      - title: artwork title
      - from: previous owner (or "SYSTEM")
      - to: recipient owner
    """
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain: List[Block] = [self._create_genesis_block()]
        self.current_owner: Dict[str, str] = {}   # asset_hash -> owner
        self.history: Dict[str, List[Dict]] = {}  # asset_hash -> list of transactions
        self.assets_meta: Dict[str, Dict] = {}    # asset_hash -> {filename, title}

    def _create_genesis_block(self) -> Block:
        tx = {
            "action": "GENESIS",
            "asset_hash": "GENESIS_ASSET",
            "filename": "",
            "title": "Genesis",
            "from": "SYSTEM",
            "to": "network"
        }
        b = Block(index=0, timestamp=now_iso(), transactions=[tx], previous_hash="0"*64)
        b.mine(difficulty=1)
        return b

    def asset_exists(self, asset_hash: str) -> bool:
        return asset_hash in self.current_owner

    def mint(self, asset_hash: str, owner: str, filename: str, title: str) -> Block:
        if self.asset_exists(asset_hash):
            raise ValueError(f"Asset '{asset_hash}' already exists; cannot mint again.")
        tx = {
            "action": "MINT",
            "asset_hash": asset_hash,
            "filename": filename,
            "title": title,
            "from": "SYSTEM",
            "to": owner
        }
        block = self._append_block([tx])
        self.current_owner[asset_hash] = owner
        self.history.setdefault(asset_hash, []).append(tx)
        self.assets_meta[asset_hash] = {"filename": filename, "title": title}
        return block

    def transfer(self, asset_hash: str, from_owner: str, to_owner: str) -> Block:
        if not self.asset_exists(asset_hash):
            raise ValueError(f"Asset '{asset_hash}' does not exist; mint first.")
        if self.current_owner.get(asset_hash) != from_owner:
            raise ValueError(f"Invalid transfer: '{from_owner}' is not the current owner of '{asset_hash}'.")
        meta = self.assets_meta.get(asset_hash, {"filename": "", "title": ""})
        tx = {
            "action": "TRANSFER",
            "asset_hash": asset_hash,
            "filename": meta.get("filename", ""),
            "title": meta.get("title", ""),
            "from": from_owner,
            "to": to_owner
        }
        block = self._append_block([tx])
        self.current_owner[asset_hash] = to_owner
        self.history.setdefault(asset_hash, []).append(tx)
        return block

    def _append_block(self, txs: List[Dict]) -> Block:
        prev = self.chain[-1]
        block = Block(index=len(self.chain), timestamp=now_iso(), transactions=txs, previous_hash=prev.hash)
        block.mine(self.difficulty)
        # log mined block for visibility (printed in server console)
        print(f"[MINE] index={block.index} nonce={block.nonce} hash={block.hash}")
        self.chain.append(block)
        return block

    def is_valid(self) -> bool:
        # verify links, recompute hashes and PoW
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr.previous_hash != prev.hash:
                return False
            if curr.calculate_hash() != curr.hash:
                return False
            if not curr.hash.startswith("0"*self.difficulty):
                return False

        # replay the full chain to ensure ownership rules were followed
        owners: Dict[str, str] = {}
        for blk in self.chain:
            for tx in blk.transactions:
                asset = tx["asset_hash"]
                if tx["action"] == "MINT":
                    if asset in owners:
                        # duplicate mint
                        return False
                    owners[asset] = tx["to"]
                elif tx["action"] == "TRANSFER":
                    if asset not in owners:
                        return False
                    if owners[asset] != tx["from"]:
                        return False
                    owners[asset] = tx["to"]
                else:
                    # GENESIS or others -> ignore
                    pass

        # optionally compare replayed owners with stored current_owner (if needed)
        return True

    def list_assets(self) -> List[Dict]:
        out = []
        for h, meta in self.assets_meta.items():
            out.append({
                "asset_hash": h,
                "title": meta.get("title"),
                "filename": meta.get("filename"),
                "owner": self.current_owner.get(h)
            })
        return out

    def get_history(self, asset_hash: str) -> List[Dict]:
        return self.history.get(asset_hash, [])
