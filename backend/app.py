from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import LeadRequest, ChatRequest
from grok_service import analyze_lead
from chat_service import chat_with_doctyn

app = FastAPI(
    title="Doctyn AI Lead Intelligence Bot",
    description="Intermediate demo for Doctyn Academy"
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
        "message": "Doctyn AI Lead Intelligence Bot is active"
    }

@app.post("/analyze-lead")
def analyze(lead: LeadRequest):
    result = analyze_lead(lead.model_dump())

    return {
        "success": True,
        "analysis": result
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = chat_with_doctyn(request.message)

    return {
        "success": True,
        "response": result
    }
