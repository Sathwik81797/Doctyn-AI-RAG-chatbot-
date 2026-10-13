from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models_v2 import ChatRequestV2
from chat_service_v3 import chat_with_doctyn_v3


app = FastAPI(
    title="Doctyn AI Knowledge Assistant V3",
    description="RAG chatbot powered by Doctyn PDFs and website knowledge",
    version="3.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "status": "running",
        "version": "3.0",
        "message": "Doctyn AI RAG Assistant is active"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "knowledge": "loaded"
    }


@app.post("/chat")
def chat(request: ChatRequestV2):
    result = chat_with_doctyn_v3(
        message=request.message,
        session_id=request.session_id,
        page_context=request.page_context
    )

    return {
        "success": True,
        "response": result
    }
