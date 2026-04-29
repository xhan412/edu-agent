from fastapi import FastAPI
from src.models import WorkflowRequest, WorkflowResult
from src.orchestrator import EduAgentOrchestrator

app = FastAPI(
    title="Edu Agent Mimo Demo",
    description="Multi-agent educational content generation workflow demo.",
    version="0.1.0",
)

orchestrator = EduAgentOrchestrator()


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "project": "Edu Agent Mimo Demo",
        "description": "Multi-agent workflow for educational infographic prompt generation and QA."
    }


@app.post("/workflow/generate", response_model=WorkflowResult)
def generate_workflow(request: WorkflowRequest):
    return orchestrator.run(request)
