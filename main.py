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
/* EduGenie - Final Styled CSS */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
    color: #333;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

h1 {
    color: white;
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

p {
    text-align: center;
    color: white;
    margin-bottom: 25px;
    font-size: 1.1rem;
}

.task-selector {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 0 auto 20px;
    width: 90%;
    max-width: 650px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.task-selector select {
    padding: 12px 15px;
    border-radius: 8px;
    border: 2px solid #667eea;
    font-size: 16px;
    width: 70%;
    margin-top: 10px;
    cursor: pointer;
    background: white;
}

form {
    background: white;
    padding: 25px;
    margin: 20px auto;
    width: 90%;
    max-width: 650px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

label {
    font-size: 1.1rem;
    color: #4a5af9;
}

input[type="text"], textarea, select {
    width: 100%;
    padding: 12px 15px;
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    font-size: 16px;
    margin: 10px 0;
    outline: none;
    transition: 0.3s;
}

input[type="text"]:focus, textarea:focus {
    border-color: #667eea;
}

button {
    width: 100%;
    padding: 13px 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
    transition: 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a6fd5, #6a42a0);
}

.output {
    margin: 0 auto 25px;
    width: 90%;
    max-width: 650px;
    background: #fff;
    padding: 18px;
    border-radius: 12px;
    min-height: 20px;
    border-left: 5px solid #667eea;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: left;
    white-space: pre-wrap;
}

/* Responsive Design - Photo la ketta requirement */
@media (max-width: 600px) {
    h1 { font-size: 1.8rem; }
    form, .task-selector, .output { width: 95%; }
    .task-selector select { width: 100%; }
}
