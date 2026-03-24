import json
from openai import AsyncOpenAI
from config import settings
from models.schemas import ReviewIssue, ReviewSummary, ReviewResponse
from services.prompt import build_system_prompt, build_user_prompt


# Create one OpenAI client — shared across all requests
# We create it once here instead of inside the function
# so we don't recreate it on every single API call
client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url="https://api.groq.com/openai/v1",
)


async def run_review(
    pr_url: str,
    pr_data: dict,
    focus_areas: list[str]
) -> ReviewResponse:
    """
    The full review pipeline:
    1. Build prompts
    2. Call GPT
    3. Parse response
    4. Return structured result
    """

    # Step 1 — Build both prompts
    system_prompt = build_system_prompt(focus_areas)
    user_prompt = build_user_prompt(pr_data)

    # Step 2 — Call OpenAI
    response = await client.chat.completions.create(
        model=settings.openai_model,
        max_tokens=settings.max_tokens,
        temperature=0.2,        # low = more precise, less creative
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        response_format={"type": "json_object"},  # forces valid JSON output
    )

    # Step 3 — Extract the text from GPT's response
    raw = response.choices[0].message.content

    # Step 4 — Convert JSON text into a Python dictionary
    data = json.loads(raw)

    # Step 5 — Convert each issue dict into a ReviewIssue object
    issues = [ReviewIssue(**issue) for issue in data.get("issues", [])]

    # Step 6 — Count issues by severity
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        counts[issue.severity] += 1

    # Step 7 — Build the summary
    summary = ReviewSummary(
        total_issues=len(issues),
        critical=counts["critical"],
        high=counts["high"],
        medium=counts["medium"],
        low=counts["low"],
        overall_assessment=data.get(
            "overall_assessment",
            "No overall assessment provided."
        ),
    )

    # Step 8 — Return the complete response
    return ReviewResponse(
        pr_title=pr_data["title"],
        pr_url=pr_url,
        issues=issues,
        summary=summary,
    )