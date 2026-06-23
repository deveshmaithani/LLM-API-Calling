# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os, json
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI(title="AI Code Reviewer")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str = "java"  # default java, but supports others

@app.post("/review")
async def review_code(request: CodeRequest):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a senior {request.language} engineer.
                Review code and respond ONLY in JSON:
                {{
                    "overall_score": <1-10>,
                    "summary": "<verdict>",
                    "bugs": [],
                    "performance_issues": [],
                    "security_vulnerabilities": [],
                    "bad_practices": [],
                    "suggestions": [],
                    "improved_code": "<fixed version>"
                }}"""
            },
            {
                "role": "user",
                "content": f"Review:\n\n{request.code}"
            }
        ],
        temperature=0.3
    )
    raw = response.choices[0].message.content
    clean = raw.strip().replace("```json","").replace("```","").strip()
    return json.loads(clean)

@app.get("/")
def root():
    return {"message": "AI Code Reviewer is running"}

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)