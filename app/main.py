from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
uploads_dir = Path("/app/uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # today auto-fills; we’ll replace with OCR later
    today = datetime.now().strftime("%Y-%m-%d")
    return templates.TemplateResponse("index.html", {"request": request, "today": today})

@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...), access_code: str = Form("")):
    # simple access gate (optional): set ACCESS_CODE env later; for now accept anything
    data = await file.read()
    dest = uploads_dir / file.filename
    dest.write_bytes(data)

    # placeholder: pretend we extracted Count Date = today
    count_date = datetime.now().strftime("%Y-%m-%d")

    return HTMLResponse(f"""
        <h3>Upload received</h3>
        <p>File saved: {dest.name}</p>
        <p><b>Count Date (placeholder):</b> {count_date}</p>
        <p>Next: we’ll add OCR + the 7 half-life filter and 10× natural isotope check.</p>
        <p><a href="/">Back</a></p>
    """)
