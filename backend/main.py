from fastapi import FastAPI,Request,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import uuid
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils.extraction import load_pdf_text
import os


app = FastAPI()

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
    
@app.get("/upload-pdf")

async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        temp_file_path = f"telp_{file_id}.pdf"
        
        #Save file 
        with open(temp_file_path,"wb") as f:
            f.write(await file.read())
            
        extracted_text = load_pdf_text(temp_file_path)
        
        return JSONResponse(content = {
            "text":extracted_text
            })
    except Exception as e:
        return JSONResponse(status_code=500,content = {"error":str(e)})
        
    
    
    
    
    
    
    