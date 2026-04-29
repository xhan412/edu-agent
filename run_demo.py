import json
from pathlib import Path
from rich import print_json
from src.orchestrator import EduAgentOrchestrator
from src.models import WorkflowRequest


def main():
    sample_path = Path("examples/sample_request.json")
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    request = WorkflowRequest(**data)

    orchestrator = EduAgentOrchestrator()
    result = orchestrator.run(request)

    print_json(data=result.model_dump())


if __name__ == "__main__":
    main()
