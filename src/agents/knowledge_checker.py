from src.models import ParsedContent, CheckReport
from .base import BaseAgent


class KnowledgeCheckerAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "KnowledgeCheckerAgent"

    def run(self, parsed: ParsedContent) -> CheckReport:
        issues = []
        suggestions = []

        if "早读版" in parsed.lesson_title:
            suggestions.append("标题中包含早读版，需要确认图片标题是否需要显示该标记。")

        if len(parsed.raw_terms) > 60:
            suggestions.append("词语数量较多，建议拆成多页，避免页面过密。")

        for kp in parsed.knowledge_points:
            joined = "".join(kp.get("items", []))
            if len(joined) > 500:
                issues.append({
                    "type": "density",
                    "message": f"知识点「{kp.get('title')}」内容较密，建议拆分。"
                })

        return CheckReport(
            passed=len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
        )
