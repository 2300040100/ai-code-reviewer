from pydantic import BaseModel
from typing import Literal


class ReviewRequest(BaseModel):
    pr_url: str
    focus_areas: list[Literal["bugs", "performance", "style", "security"]] = [
        "bugs", "performance", "style", "security"
    ]


class ReviewIssue(BaseModel):
    category: Literal["bug", "performance", "style", "security"]
    severity: Literal["critical", "high", "medium", "low"]
    file: str
    line: str
    title: str
    description: str
    suggestion: str


class ReviewSummary(BaseModel):
    total_issues: int
    critical: int
    high: int
    medium: int
    low: int
    overall_assessment: str


class ReviewResponse(BaseModel):
    pr_title: str
    pr_url: str
    issues: list[ReviewIssue]
    summary: ReviewSummary