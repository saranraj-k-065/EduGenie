import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie API", version="1.0.0",
              description="Gemini-powered educational learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory="templates")


class TaskRequest(BaseModel):
    task: Literal["explain", "qa", "quiz", "summarize", "learn"]
    text: str = Field(min_length=1, max_length=20000)
    level: str = Field(default="Beginner", max_length=40)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: TaskRequest):
    return {"result": answer_question(payload.text, payload.level)}


@app.post("/explain")
async def explain(payload: TaskRequest):
    return {"result": explain_concept(payload.text, payload.level)}


@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return {"result": generate_quiz(payload.text, payload.level)}


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return {"result": summarize_text(payload.text, payload.level)}


@app.post("/learn/recommendations")
async def recommendations(payload: TaskRequest):
    return {"result": get_learning_recommendations(payload.text, payload.level)}


@app.post("/api/task")
async def run_task(payload: TaskRequest):
    """Single frontend endpoint dispatching to the documented feature modules."""

    funcs = {
        "qa": answer_question,
        "explain": explain_concept,
        "quiz": generate_quiz,
        "summarize": summarize_text,
        "learn": get_learning_recommendations,
    }

    try:
        result = funcs[payload.task](
            payload.text,
            payload.level
        )

        return {
            "task": payload.task,
            "result": result
        }

    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )