from fastapi import FastAPI,Request,UploadFile,File,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uuid
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from backend.utils.extraction import load_pdf_text,extract_text_from_url
from backend.utils.summarize import summarize_text
import traceback
import tempfile

import os


app = FastAPI()

class TextRequest(BaseModel):
    text: str

origins = [
    "http://localhost:8501/"
]

#Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
async def test_working():
    return ({'message':'The site is working!'})

    
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Save uploaded PDF bytes to a temp file (delete=False to keep while processing)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        try:
            tmp.write(contents)
            tmp.flush()
            tmp.close()  # close for access by other processes

            # Extract text from the temp PDF file
            extracted_text = load_pdf_text(tmp.name)

            # Optional: fallback if empty text
            if not extracted_text.strip():
                extracted_text = "[No extractable text found]"
            
             # Summarize extracted text
            summary = summarize_text(extracted_text)

        finally:
            os.unlink(tmp.name)  # Clean up temp file

        return {
            "filename": file.filename,
            "size_bytes": len(contents),
            "extracted_text": extracted_text,
            "summary": summary,
            "message": "PDF processed and summarized successfully"
        }

    except Exception as e:
        tb = traceback.format_exc()
        print("[ERROR] Exception during PDF processing:\n", tb)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
        

@app.post("/fetch-url")
async def fetch_url(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        
        if not url:
            return JSONResponse(status_code=400,content = {"error":"URL is required"})
        
        extracted_text = extract_text_from_url(url)
        summarized_text = summarize_text(extracted_text)
        
        return JSONResponse(content = {
            "text":extract_text_from_url,
            "summary":summarized_text
        })
        
    except Exception as e:
        return JSONResponse(status_code="500",content = {"error":f"PDF processing error: {e}"})
    
    
