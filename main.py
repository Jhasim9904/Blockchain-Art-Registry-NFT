# main.py
import os
import hashlib
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict

from blockchain import ArtChain, sha256_hex  # import the chain class and helper

# Create folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Digital Art Blockchain (Mini-NFT)")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Initialize chain
CHAIN = ArtChain(difficulty=2)


# Helper: compute sha256 from bytes
def file_hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --- Routes ---
@app.get("/")
async def index(request: Request):
    # pass chain and assets to template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chain": CHAIN.chain,
        "assets": CHAIN.list_assets()
    })


@app.post("/upload")
async def upload_art(request: Request,
                     title: str = Form(...),
                     owner: str = Form(...),
                     file: UploadFile = File(...)):
    """
    Upload image file (jpg/png). Server computes SHA256(file_bytes).
    If new -> save file as uploads/<hash><ext> and mint on chain.
    If already exists -> reject as duplicate.
    """
    content = await file.read()
    if not content:
        return JSONResponse({"message": "Empty file"}, status_code=400)

    # compute hash
    asset_hash = file_hash_bytes(content)
    # keep original extension where possible
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower() if ext else ""
    save_name = f"{asset_hash}{ext}"
    save_path = os.path.join(UPLOAD_DIR, save_name)

    # duplicate prevention
    if CHAIN.asset_exists(asset_hash):
        return JSONResponse({"message": f"Asset already exists (hash: {asset_hash})."}, status_code=400)

    # save file
    with open(save_path, "wb") as f:
        f.write(content)

    # Mint on chain
    CHAIN.mint(asset_hash=asset_hash, owner=owner, filename=save_name, title=title)
    return RedirectResponse("/", status_code=303)


@app.get("/transfer")
async def transfer_form(request: Request):
    # transfer page with asset list
    return templates.TemplateResponse("transfer.html", {
        "request": request,
        "assets": CHAIN.list_assets()
    })


@app.post("/transfer")
async def do_transfer(asset_hash: str = Form(...),
                      sender: str = Form(...),
                      recipient: str = Form(...)):
    try:
        CHAIN.transfer(asset_hash=asset_hash, from_owner=sender, to_owner=recipient)
        return RedirectResponse("/", status_code=303)
    except ValueError as e:
        return JSONResponse({"message": str(e)}, status_code=400)


@app.get("/chain")
async def get_chain():
    out = []
    for b in CHAIN.chain:
        out.append({
            "index": b.index,
            "timestamp": b.timestamp,
            "transactions": b.transactions,
            "previous_hash": b.previous_hash,
            "nonce": b.nonce,
            "hash": b.hash
        })
    return {"chain": out, "valid": CHAIN.is_valid()}


@app.get("/asset/{asset_hash}")
async def asset_info(asset_hash: str):
    meta = CHAIN.assets_meta.get(asset_hash)
    if not meta:
        return JSONResponse({"message": "Asset not found"}, status_code=404)
    return {
        "asset_hash": asset_hash,
        "meta": meta,
        "owner": CHAIN.current_owner.get(asset_hash),
        "history": CHAIN.get_history(asset_hash)
    }
