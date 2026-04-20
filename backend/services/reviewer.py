import json
from openai import AsyncOpenAI
from config import settings
from models.schemas import ReviewIssue, ReviewSummary, ReviewResponse, PRStats
from services.prompt import build_system_prompt, build_user_prompt

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url="https://api.groq.com/openai/v1",
)


def chunk_files(files: list, max_files: int = 20) -> list[list]:
    """Split files into chunks so large PRs don't exceed token limits."""
    return [files[i:i + max_files] for i in range(0, len(files), max_files)]


async def run_review(
    pr_url: str,
    pr_data: dict,
    focus_areas: list[str]
) -> ReviewResponse:

    all_issues = []
    overall_assessment = "No overall assessment provided."
    files = pr_data["files"]

    # Split into chunks of 20 files each
    chunks = chunk_files(files, max_files=20)

    for i, chunk in enumerate(chunks):

        chunk_data = {**pr_data, "files": chunk}
        system_prompt = build_system_prompt(focus_areas)
        user_prompt = build_user_prompt(chunk_data)

        response = await client.chat.completions.create(
            model=settings.openai_model,
            max_tokens=settings.max_tokens,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        chunk_issues = [
            ReviewIssue(**issue)
            for issue in data.get("issues", [])
        ]
        all_issues.extend(chunk_issues)

        # Only use assessment from first chunk
        if i == 0:
            overall_assessment = data.get(
                "overall_assessment",
                "No overall assessment provided."
            )

 
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in all_issues:
        counts[issue.severity] += 1

    summary = ReviewSummary(
        total_issues=len(all_issues),
        critical=counts["critical"],
        high=counts["high"],
        medium=counts["medium"],
        low=counts["low"],
        overall_assessment=overall_assessment,
    )


    stats = PRStats(
        author=pr_data["author"],
        base_branch=pr_data["base_branch"],
        head_branch=pr_data["head_branch"],
        files_reviewed=len(files),
        total_additions=pr_data.get("total_additions", 0),
        total_deletions=pr_data.get("total_deletions", 0),
    )


    return ReviewResponse(
        pr_title=pr_data["title"],
        pr_url=pr_url,
        stats=stats,
        issues=all_issues,
        summary=summary,
    )
