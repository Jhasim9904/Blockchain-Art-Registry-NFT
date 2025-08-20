# Simple-Blockchain-Implementation

A beginner-friendly blockchain implementation written in python.
This project demonstrates the core concepts of blockchain, cryptocurrency, and mining using Python and its libraries.

## 🚀 Features
- ✅ Genesis block creation (first block in the chain)  
- ✅ Add transactions (sender → receiver, amount)  
- ✅ Mine blocks using Proof of Work (difficulty-based)  
- ✅ Mining reward system (reward goes to miner)  
- ✅ Blockchain validation (detects tampering)  
- ✅ Interactive CLI menu to test features  
- ✅ Pretty-printed blockchain view  

## ⚙️ How It Works
1. **Transactions** are added to a pool.  
2. **Mining a block**:  
   - All pending transactions are added into a block.  
   - Miner solves a Proof of Work puzzle (hash starts with `000`).  
   - Miner receives a reward transaction (like cryptocurrency).  
3. **Blocks are linked** with cryptographic hashes.  
4. **Validation** checks if the chain is intact (tamper-proof).  

**Concepts used**:
Blockchain basics (linked blocks),
SHA-256 hashing for block security,
Proof of Work mining,
Reward system (cryptocurrency simulation),
Tamper detection with validation.


