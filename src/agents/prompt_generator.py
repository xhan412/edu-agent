from typing import List
from src.models import PagePlan, PromptResult, RulePlan, WorkflowRequest
from .base import BaseAgent


class PromptGeneratorAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "PromptGeneratorAgent"

    def run(self, request: WorkflowRequest, page_plans: List[PagePlan], rule_plan: RulePlan) -> List[PromptResult]:
        results: List[PromptResult] = []

        for page in page_plans:
            locked_text = []
            if page.title:
                locked_text.append(page.title)
            locked_text.append(page.subtitle)
            locked_text.extend(page.content_blocks)

            prompt = self._build_prompt(request, page, rule_plan)

            results.append(PromptResult(
                page_id=page.page_id,
                image_prompt_en=prompt,
                locked_text_zh=locked_text,
                negative_constraints=[
                    "Do not invent Chinese text.",
                    "Do not omit any locked text.",
                    "Do not change pinyin tone marks.",
                    "Do not create overcrowded layout.",
                    "Do not use Traditional Chinese.",
                    "Do not use heavy poster style.",
                ],
            ))

        return results

    def _build_prompt(self, request: WorkflowRequest, page: PagePlan, rule_plan: RulePlan) -> str:
        title_part = f'Main title: "{page.title}".' if page.title else "No main lesson title on this page."
        content = "\n".join([f"- {x}" for x in page.content_blocks])

        style = request.style_reference or (
            "premium hand-drawn Chinese educational infographic, soft cream paper background, "
            "clean colored-pencil texture, fine ink outlines, elegant card-based layout, "
            "gentle cloud motifs, small restrained decorative icons, highly readable workbook aesthetics"
        )

        return f"""
Create a high-quality educational infographic page for {request.grade} {request.subject}.

Page ID: {page.page_id}
Task type: {request.task_type}

Style:
{style}

Title rules:
{title_part}
Subtitle: "{page.subtitle}"

Locked Simplified Chinese content:
{content}

Layout instruction:
{page.layout_advice}

Hard constraints:
- Use Simplified Chinese only inside the image.
- Preserve every locked Chinese word exactly.
- Follow page ID {page.page_id}.
- Keep the layout clean, readable, and not overcrowded.
- Use refined hand-drawn teaching sheet aesthetics, not a heavy poster.
- Avoid wrong pinyin, missing text, wrong title hierarchy, and inconsistent page numbering.
""".strip()
