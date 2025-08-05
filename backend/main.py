from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import time 

app = FastAPI()

origins = [
    "http://localhost:8501/"
]

#Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)