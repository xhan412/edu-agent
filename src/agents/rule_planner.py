from src.models import ParsedContent, WorkflowRequest, RulePlan
from .base import BaseAgent


class RulePlannerAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "RulePlannerAgent"

    def run(self, request: WorkflowRequest, parsed: ParsedContent) -> RulePlan:
        hard_constraints = [
            "图片中只允许使用简体中文，必要科学符号和拼音除外。",
            "所有用户提供的教材内容必须作为锁定文本，不得擅自改写。",
            "页码采用 X-Y：X 为具体知识点序号，Y 为该知识点下的页面序号。",
            "除每个知识点第一张图外，延伸页不显示课文大标题，只显示该页小标题。",
            "如果内容过密，必须拆页，不允许硬塞到单页。",
        ]
        hard_constraints.extend(request.strict_rules)

        return RulePlan(
            page_id_strategy="X-Y numbering. X = knowledge point index, Y = page index within that point.",
            title_strategy="First page of a knowledge point can show main lesson title; extension pages only show subtitle.",
            language_strategy="Use Simplified Chinese inside images. Generate external image prompt in English.",
            validation_strategy=[
                "拼音声调校验",
                "错别字校验",
                "标题层级校验",
                "内容完整性校验",
                "页面密度校验",
                "风格一致性校验",
            ],
            hard_constraints=hard_constraints,
        )
