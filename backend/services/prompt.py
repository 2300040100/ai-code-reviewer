# This dictionary maps each focus area to a detailed description
# that tells GPT exactly what to look for
FOCUS_AREA_DESCRIPTIONS = {
    "bugs": (
        "Bug Detection — identify logic errors, null pointer risks, "
        "off-by-one errors, unhandled exceptions, race conditions."
    ),
    "performance": (
        "Performance Issues — spot inefficient algorithms, "
        "unnecessary database queries in loops (N+1 problem), "
        "memory leaks, blocking I/O in async contexts."
    ),
    "style": (
        "Code Style & Best Practices — flag naming inconsistencies, "
        "overly complex functions, missing docstrings, dead code, "
        "violation of SOLID and DRY principles."
    ),
    "security": (
        "Security Vulnerabilities — detect SQL injection, XSS, "
        "hardcoded secrets, missing input validation, "
        "improper authentication or authorization checks."
    ),
}


def build_system_prompt(focus_areas: list[str]) -> str:
    """
    Builds the system prompt — tells GPT what role to play
    and exactly what rules to follow.
    """
    # Build a bullet list of only the selected focus areas
    focus_lines = "\n".join(
        f"- {FOCUS_AREA_DESCRIPTIONS[area]}"
        for area in focus_areas
        if area in FOCUS_AREA_DESCRIPTIONS
    )

    return f"""You are an expert senior software engineer doing a thorough code review.
Analyze the GitHub pull request diff and find issues in these categories:

{focus_lines}

Respond ONLY with a valid JSON object in this exact format:
{{
  "issues": [
    {{
      "category": "bug" | "performance" | "style" | "security",
      "severity": "critical" | "high" | "medium" | "low",
      "file": "<filename>",
      "line": "<line number or range like 42-48>",
      "title": "<short issue title>",
      "description": "<clear explanation of the problem>",
      "suggestion": "<concrete fix or improvement>"
    }}
  ],
  "overall_assessment": "<2-3 sentence summary of PR quality>"
}}

Rules you must follow:
- Only report REAL issues visible in the diff. Never invent problems.
- critical = must fix before merging (security breach, data loss risk).
- high = will likely cause bugs in production.
- medium = degrades quality but won't immediately break things.
- low = minor style or readability improvement.
- Output ONLY the JSON. No markdown fences. No explanation. Just JSON.
"""


def build_user_prompt(pr_data: dict) -> str:
    """
    Builds the user prompt — the actual PR content
    we want GPT to analyze.
    """
    # Format each changed file with its diff
    file_sections = []
    for f in pr_data["files"]:
        file_sections.append(
            f"### File: {f['filename']} "
            f"({f['status']}, +{f['additions']} -{f['deletions']})\n"
            f"```diff\n{f['patch']}\n```"
        )

    files_text = "\n\n".join(file_sections)

    return f"""PR Title: {pr_data['title']}
PR Description: {pr_data['description']}
Author: {pr_data['author']}
Branches: {pr_data['base_branch']} <- {pr_data['head_branch']}

--- CHANGED FILES ---

{files_text}
"""