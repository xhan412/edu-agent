import re
from typing import List, Dict, Any
from src.models import WorkflowRequest, ParsedContent
from .base import BaseAgent


class ContentParserAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ContentParserAgent"

    def run(self, request: WorkflowRequest) -> ParsedContent:
        lines = [x.strip() for x in request.source_text.splitlines() if x.strip()]

        knowledge_points: List[Dict[str, Any]] = []
        current = None

        heading_pattern = re.compile(r"^[一二三四五六七八九十]+[、.．]|^\d+[、.．]")

        for line in lines:
            if heading_pattern.match(line):
                current = {
                    "title": line,
                    "items": []
                }
                knowledge_points.append(current)
            elif current:
                current["items"].append(line)
            else:
                knowledge_points.append({
                    "title": "未分组内容",
                    "items": [line]
                })

        terms = re.findall(r"[\u4e00-\u9fa5]{2,8}", request.source_text)

        warnings = []
        if not knowledge_points:
            warnings.append("没有识别到清晰的知识点结构，需要人工确认。")

        return ParsedContent(
            subject=request.subject,
            grade=request.grade,
            lesson_title=request.lesson_title,
            task_type=request.task_type,
            knowledge_points=knowledge_points,
            raw_terms=terms[:80],
            warnings=warnings,
        )
