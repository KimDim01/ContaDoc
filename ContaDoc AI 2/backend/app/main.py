from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from app.services.document_processor import processor
from app.services.vector_store import vector_store
from app.services.rag_engine import rag_engine
from app.services.extraction_service import extraction_service
from app.services.auth_service import auth_handler
from app.services.audit_logger import audit_logger
from app.services.hf_service import hf_client
from app.core.config import settings
import shutil
import os
import uuid

app = FastAPI(title=settings.PROJECT_NAME)

# Dependency for Auth
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")
    token = authorization.replace("Bearer ", "")
    user = auth_handler.decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

@app.get("/")
async def root():
    return {"message": "ContaDoc AI Enterprise API is running"}

@app.get("/validate-api")
async def validate_api():
    """
    Validates the Hugging Face API Token and lists available models.
    """
    return hf_client.validate_and_list_models()

@app.post("/login")
async def login(username: str, password: str):
    # In a real app, check against a database. Here we use a simple mock.
    if username == "admin" and password == "admin123":
        token = auth_handler.create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/upload/{client_id}")
async def upload_document(client_id: str, file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    """
    Uploads a document, processes it, and stores it in the vector database.
    """
    client_dir = os.path.join(settings.UPLOAD_DIR, client_id)
    os.makedirs(client_dir, exist_ok=True)

    file_path = os.path.join(client_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks = processor.process_file(file_path)

        metadatas = [{"source": file.filename} for _ in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]

        vector_store.add_documents(client_id, chunks, metadatas, ids)

        audit_logger.log_action(user['sub'], "UPLOAD", client_id, f"Uploaded file: {file.filename}")

        return {
            "filename": file.filename,
            "chunks_created": len(chunks),
            "status": "success",
            "message": f"Document indexed and stored for client {client_id}."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/{client_id}")
async def ask_question(client_id: str, query: str, user: dict = Depends(get_current_user)):
    """
    Ask a question about a specific client's documents.
    """
    try:
        response = await rag_engine.answer_question(client_id, query)
        audit_logger.log_action(user['sub'], "QUERY", client_id, f"Question: {query}")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/{client_id}")
async def extract_data(client_id: str, prompt: str, user: dict = Depends(get_current_user)):
    """
    Extracts structured data from documents and generates an Excel report.
    """
    try:
        result = await extraction_service.extract_structured_data(client_id, prompt)
        audit_logger.log_action(user['sub'], "EXTRACTION", client_id, f"Prompt: {prompt}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
