from fastapi import FastAPI, UploadFile, File, Form, HTTPException,APIRouter
from pypdf import PdfReader
from typing import List, Dict, Any
import httpx
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://34.132.46.72:8080"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

EMBEDDING_SERVICE_URL = "http://embeddings:8002/generate_embeddings"

class DocumentInput(BaseModel):
    chat_id: int
    titulo: str
    texto: str
    rating: float

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

@router.post("/upload_document")
async def upload_document(data: DocumentInput) -> Dict[str, Any]:
    try:
        if not data.texto.strip():
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

        # Construir el payload: lista con un solo elemento
        payload = {
            "chat_id": data.chat_id,
            "title": data.titulo,
            "chunks": [f"{data.texto}"],
            "rating": data.rating
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(EMBEDDING_SERVICE_URL, json=payload)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
app.include_router(router)