from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import functions from app.py (Munnadi panna 5 modules)
from app import (
    explain_topic,
    answer_question,
    generate_quiz,
    summarize_text,
    get_learning_recommendations
)

app = FastAPI(
    title="EduGenie - AI Learning Assistant API",
    description="Backend API for Explanation, QnA, Quiz, Summary and Learning Path",
    version="1.0.0"
)

# CORS - Frontend connect panna thevai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for POST request
class TopicRequest(BaseModel):
    topic: str

class TextRequest(BaseModel):
    text: str

# 1. Root API - Health Check
@app.get("/")
async def root():
    return {
        "message": "Welcome to EduGenie API 🚀",
        "status": "API is running",
        "endpoints": ["/qa", "/explain/", "/summarize/", "/quiz", "/learn/recommendations"]
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 2. Q&A Module - GET /qa?question=...
@app.get("/qa")
async def qa_api(question: str = Query(..., description="Enter your question")):
    try:
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        answer = answer_question(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Explanation Module - POST /explain/
@app.post("/explain/")
async def explain_api(request: TopicRequest):
    try:
        if not request.topic.strip():
            return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
        explanation = explain_topic(request.topic)
        return {"topic": request.topic, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Summarize Module - POST /summarize/
@app.post("/summarize/")
async def summarize_api(request: TextRequest):
    try:
        if not request.text.strip():
            return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
        summary = summarize_text(request.text)
        return {"original_length": len(request.text), "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Quiz Module - POST /quiz
@app.post("/quiz")
async def quiz_api(request: TextRequest):
    try:
        if not request.text.strip():
            return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
        quiz_data = generate_quiz(request.text)
        return {"quiz": quiz_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Learning Path Module - GET /learn/recommendations?topic=...
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(..., description="Enter topic for learning path")):
    try:
        if not topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        recommendations = get_learning_recommendations(topic)
        return {"topic": topic, "recommendations": recommendations, "learning_path": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
