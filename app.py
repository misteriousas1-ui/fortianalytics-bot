from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn, os
from scanner import analyze_symbol

app = FastAPI()

def is_premium(code):
    if not os.path.exists("sandi.txt"):
        print("DEBUG: File sandi.txt tidak ditemukan!")
        return False
    with open("sandi.txt", "r", encoding="utf-8") as f:
        sandi_tersimpan = f.read().strip().upper()
    
    input_code = str(code).strip().upper()
    
    # TAMBAHAN DEBUG: Lihat di terminal server Anda
    print(f"DEBUG: Sandi di file='{sandi_tersimpan}', Input dari web='{input_code}'")
    print(f"DEBUG: Status Kecocokan = {input_code == sandi_tersimpan}")
    
    return input_code == sandi_tersimpan

@app.get("/signals")
def get_signals(q: str = "BTC", code: str = "0"):
    # Jika is_premium TRUE, beri akses q (pair apa saja), jika FALSE paksa BTC
    if is_premium(code):
        symbol_to_fetch = q.upper()
        status = "PREMIUM"
    else:
        symbol_to_fetch = "BTC"
        status = "BASIC"
    
    return {"data": [analyze_symbol(symbol_to_fetch)], "status": status}

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)