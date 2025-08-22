# ArtChain - Mini NFT Ledger on Blockchain (Digital Art Registry)

ArtChain is a blockchain-powered web application built with FastAPI that allows users to upload digital artworks. Each uploaded artwork is stored immutably on a blockchain-like structure, ensuring authenticity, transparency, and preventing tampering.
Each artwork is stored with a **unique cryptographic hash**, ensuring immutability and uniqueness — acting as a **mini NFT ledger**.


## 🚀 Features
- 📂 **Upload artwork files** (PNG, JPG, JPEG).  
- 🔐 Generate a **unique SHA-256 hash** for each artwork.  
- 🚫 Prevent duplicate uploads with blockchain hash verification.  
- ⛓ Store each artwork as a **block in a tamper-proof blockchain ledger**.  
- 👤 Record **ownership details** of each uploaded artwork.  
- 🔄 **Transfer ownership** of an artwork (simulating NFT transfers).  
- 📑 **View full blockchain ledger** with metadata (hash, owner, timestamp).  
- 🌐 Web interface built with **HTML + FastAPI** templates.
- 🛑 If you upload the same file again → system rejects it: by displaying json
{
  "message": "Asset already exists (hash: <hash>)"
}

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)  
- **Blockchain Core:** Custom Python implementation (`blockchain.py`)  
- **Frontend:** HTML (Jinja2 Templates)  
- **Storage:** Local filesystem (`static/uploads/`)  
- **Server:** Uvicorn  

## ⚙️ How It Works

1. **Upload Artwork**  
   - User uploads an image (PNG, JPG, JPEG).  
   - A **SHA-256 hash** is generated for the file.  

2. **Block Creation**  
   - A new block is created with:  
     - File name  
     - Hash  
     - Timestamp  
     - Owner details  

3. **Duplicate Check**  
   - The system checks if the hash already exists.  
   - If yes → ❌ Upload rejected (ensures immutability).  
   - If no → ✅ Block is added to the chain.  

4. **Ledger Update**  
   - The blockchain acts as a **mini NFT ledger**.  
   - You can view the **entire history** of all uploaded artworks.  

5. **Ownership Transfer**  
   - Ownership of any artwork can be **transferred**.  
   - Blockchain records the new owner while **preserving old history**.  
 


## 🔗 Blockchain Concepts Used

### 🔐 Hashing
- Each artwork gets a **SHA-256 hash**, acting as a digital fingerprint.  
- Ensures **uniqueness** and **integrity** of files.  

### 🛡 Immutability
- Once a block is added, it **cannot be changed**.  
- Any attempt to re-upload the same file is **rejected**.  

### ⚖ Consensus Simulation
- While no mining/validators exist here,  
- The **duplicate-detection mechanism** ensures only valid, unique blocks enter the chain.  

### 📑 Ledger View
- The blockchain acts as a **mini NFT ledger**, showing:  
  - File name  
  - Hash  
  - Timestamp  
  - Current Owner  

### 🔄 Ownership Transfer
- Ownership of an artwork can be **reassigned** (like NFT resale).  
- **History is preserved** in the blockchain.  


👨‍💻 **Author**

Developed by Jhasim Hassan.

