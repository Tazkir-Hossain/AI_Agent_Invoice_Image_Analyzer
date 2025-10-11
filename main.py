from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from config import settings
from models import InvoiceResponse
from services.ocr import run_ocr
from services.parser import compose_response

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.MODEL_NAME}

@app.post("/analyze", response_model=InvoiceResponse)
async def analyze_invoice(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")
    try:
        content = await file.read()
        ocr_text, boxes = run_ocr(content)
        resp = compose_response(ocr_text, boxes)
        return JSONResponse(status_code=200, content=resp.dict())
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
