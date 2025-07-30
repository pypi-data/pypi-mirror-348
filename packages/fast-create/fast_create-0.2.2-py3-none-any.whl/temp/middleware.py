from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app import app
from starlette.middleware.base import BaseHTTPMiddleware
from database import get_db
from fastapi import Depends

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def preflight(full_path: str):
    return JSONResponse(
        content={"message": "Preflight request successful"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, PUT, DELETE, OPTIONS",  # Added GET, PUT, DELETE
            "Access-Control-Allow-Headers": "*",
        },
    )


