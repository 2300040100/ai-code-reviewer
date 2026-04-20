from pydantic import BaseModel, field_validator
from typing import Literal
import re


class ReviewRequest(BaseModel):
    pr_url: str
    focus_areas: list[Literal["bugs", "performance", "style", "security"]] = [
        "bugs", "performance", "style", "security"
    ]

    @field_validator("pr_url")
    @classmethod
    def validate_pr_url(cls, v):
        pattern = r"https://github\.com/[^/]+/[^/]+/pull/\d+"
        if not re.match(pattern, v.strip()):
            raise ValueError(
                "Invalid GitHub PR URL. "
                "Expected: https://github.com/owner/repo/pull/123"
            )
        return v.strip()

    @field_validator("focus_areas")
    @classmethod
    def validate_focus_areas(cls, v):
        if len(v) == 0:
            raise ValueError("Please select at least one focus area.")
        return v


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


# ✅ This was missing — now added!
class PRStats(BaseModel):
    author: str
    base_branch: str
    head_branch: str
    files_reviewed: int
    total_additions: int
    total_deletions: int


class ReviewResponse(BaseModel):
    pr_title: str
    pr_url: str
    stats: PRStats
    issues: list[ReviewIssue]
    summary: ReviewSummary