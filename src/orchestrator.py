from src.config import settings
from src.models import WorkflowRequest, WorkflowResult
from src.llm.mock_client import MockLLMClient
from src.llm.mimo_client import MimoClient

from src.agents.content_parser import ContentParserAgent
from src.agents.rule_planner import RulePlannerAgent
from src.agents.knowledge_checker import KnowledgeCheckerAgent
from src.agents.layout_planner import LayoutPlannerAgent
from src.agents.prompt_generator import PromptGeneratorAgent
from src.agents.quality_inspector import QualityInspectorAgent
from src.agents.optimizer import OptimizerAgent


class EduAgentOrchestrator:
    def __init__(self):
        if settings.llm_provider.lower() == "mimo":
            self.llm = MimoClient()
        else:
            self.llm = MockLLMClient()

        self.content_parser = ContentParserAgent(self.llm)
        self.rule_planner = RulePlannerAgent(self.llm)
        self.knowledge_checker = KnowledgeCheckerAgent(self.llm)
        self.layout_planner = LayoutPlannerAgent(self.llm)
        self.prompt_generator = PromptGeneratorAgent(self.llm)
        self.quality_inspector = QualityInspectorAgent(self.llm)
        self.optimizer = OptimizerAgent(self.llm)

    def run(self, request: WorkflowRequest) -> WorkflowResult:
        parsed = self.content_parser.run(request)
        rules = self.rule_planner.run(request, parsed)
        check = self.knowledge_checker.run(parsed)
        pages = self.layout_planner.run(parsed)
        prompts = self.prompt_generator.run(request, pages, rules)
        inspection = self.quality_inspector.run(prompts)
        advice = self.optimizer.run(check, inspection)

        token_estimate = {
            "parse_tokens": 800,
            "rule_plan_tokens": 600,
            "knowledge_check_tokens": 1200,
            "layout_plan_tokens": 1000,
            "prompt_generation_tokens": max(1000, len(prompts) * 800),
            "quality_inspection_tokens": max(800, len(prompts) * 500),
            "estimated_total_tokens": 4400 + len(prompts) * 1300,
            "scaling_note": "批量处理多课、多轮质检时，日消耗可达到百万级 Token。"
        }

        return WorkflowResult(
            parsed_content=parsed,
            rule_plan=rules,
            check_report=check,
            page_plans=pages,
            prompts=prompts,
            inspection_report=inspection,
            optimization_advice=advice,
            token_plan_estimate=token_estimate,
        )
