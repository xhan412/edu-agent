from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    subject: str = Field(..., description="学科，如语文、数学")
    grade: str = Field(..., description="年级，如五年级下册")
    lesson_title: str = Field(..., description="课文或知识点标题")
    task_type: str = Field(..., description="任务类型，如知识图解、背默页、拼音练习、封面")
    source_text: str = Field(..., description="用户提供的原始资料")
    style_reference: Optional[str] = Field(default=None, description="参考图风格描述")
    strict_rules: List[str] = Field(default_factory=list, description="必须遵守的生成规则")


class ParsedContent(BaseModel):
    subject: str
    grade: str
    lesson_title: str
    task_type: str
    knowledge_points: List[Dict[str, Any]]
    raw_terms: List[str]
    warnings: List[str] = []


class RulePlan(BaseModel):
    page_id_strategy: str
    title_strategy: str
    language_strategy: str
    validation_strategy: List[str]
    hard_constraints: List[str]


class CheckReport(BaseModel):
    passed: bool
    issues: List[Dict[str, str]]
    suggestions: List[str]


class PagePlan(BaseModel):
    page_id: str
    title: str
    subtitle: str
    content_blocks: List[str]
    layout_advice: str


class PromptResult(BaseModel):
    page_id: str
    image_prompt_en: str
    locked_text_zh: List[str]
    negative_constraints: List[str]


class InspectionReport(BaseModel):
    score: float
    severity: str
    detected_issues: List[Dict[str, str]]
    next_action: str


class WorkflowResult(BaseModel):
    parsed_content: ParsedContent
    rule_plan: RulePlan
    check_report: CheckReport
    page_plans: List[PagePlan]
    prompts: List[PromptResult]
    inspection_report: InspectionReport
    optimization_advice: List[str]
    token_plan_estimate: Dict[str, Any]
