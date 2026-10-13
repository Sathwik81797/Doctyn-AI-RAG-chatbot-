from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models_v2 import ChatRequestV2
from chat_service_v2 import chat_with_doctyn_v2
from course_data_v2 import get_all_courses


app = FastAPI(
    title="Doctyn AI Fellowship Assistant V2",
    description=(
        "Advanced conversational fellowship assistant "
        "for Doctyn Academy"
    ),
    version="2.0"
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
        "version": "2.0",
        "message": "Doctyn AI Fellowship Assistant V2 is active"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/courses")
def courses():
    return {
        "success": True,
        "courses": get_all_courses()
    }


@app.post("/chat")
def chat(request: ChatRequestV2):
    result = chat_with_doctyn_v2(
        message=request.message,
        session_id=request.session_id,
        page_context=request.page_context
    )

    return {
        "success": True,
        "response": result
    }
