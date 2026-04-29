from typing import List
from src.models import PromptResult, InspectionReport
from .base import BaseAgent


class QualityInspectorAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "QualityInspectorAgent"

    def run(self, prompts: List[PromptResult]) -> InspectionReport:
        detected = []

        for p in prompts:
            text_size = sum(len(x) for x in p.locked_text_zh)
            if text_size > 350:
                detected.append({
                    "page_id": p.page_id,
                    "type": "overload_risk",
                    "message": "锁定文本较多，生成图片时可能出现漏字或排版拥挤。"
                })

        score = max(0.0, 1.0 - len(detected) * 0.08)

        return InspectionReport(
            score=score,
            severity="low" if score >= 0.85 else "medium",
            detected_issues=detected,
            next_action="Proceed to image generation" if score >= 0.85 else "Split dense pages or strengthen prompt constraints",
        )
