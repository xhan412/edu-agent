from typing import List
from src.models import ParsedContent, PagePlan
from .base import BaseAgent


class LayoutPlannerAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "LayoutPlannerAgent"

    def run(self, parsed: ParsedContent) -> List[PagePlan]:
        page_plans: List[PagePlan] = []

        for i, kp in enumerate(parsed.knowledge_points, start=1):
            items = kp.get("items", [])
            title = kp.get("title", f"知识点{i}")
            chunks = self._chunk_items(items, max_chars=280)

            if not chunks:
                chunks = [[title]]

            for j, chunk in enumerate(chunks, start=1):
                page_id = f"{i}-{j}"
                show_main_title = j == 1

                page_plans.append(PagePlan(
                    page_id=page_id,
                    title=parsed.lesson_title if show_main_title else "",
                    subtitle=title,
                    content_blocks=chunk,
                    layout_advice=self._layout_advice(parsed.task_type, len("".join(chunk))),
                ))

        return page_plans

    def _chunk_items(self, items: List[str], max_chars: int) -> List[List[str]]:
        chunks: List[List[str]] = []
        current: List[str] = []
        size = 0

        for item in items:
            if size + len(item) > max_chars and current:
                chunks.append(current)
                current = [item]
                size = len(item)
            else:
                current.append(item)
                size += len(item)

        if current:
            chunks.append(current)

        return chunks

    def _layout_advice(self, task_type: str, char_count: int) -> str:
        if "背" in task_type or "默" in task_type:
            return "Use clean workbook style, large readable text cards, enough line spacing."
        if char_count > 220:
            return "Use multi-card layout with two or three sections, avoid dense paragraphs."
        return "Use elegant hand-drawn card layout with balanced whitespace."
