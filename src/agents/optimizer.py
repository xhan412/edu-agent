from typing import List
from src.models import InspectionReport, CheckReport
from .base import BaseAgent


class OptimizerAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "OptimizerAgent"

    def run(self, check_report: CheckReport, inspection_report: InspectionReport) -> List[str]:
        advice = []

        if not check_report.passed:
            advice.append("先修正知识校验问题，再进入图片生成。")

        if inspection_report.severity != "low":
            advice.append("对内容密集页继续拆分，降低单页文字量。")
            advice.append("在提示词中强化：preserve all locked text exactly, no missing words, no paraphrasing.")

        if not advice:
            advice.append("当前流程可进入图像生成阶段，生成后再进行视觉质检。")

        advice.append("建议记录每次失败案例，沉淀为负面约束库，用于下一轮自动优化。")
        return advice
