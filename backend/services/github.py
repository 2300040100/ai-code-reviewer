import httpx
import re
from config import settings


def parse_pr_url(pr_url: str) -> tuple[str, str, int]:
    """
    Breaks a GitHub PR URL into 3 parts.

    Example input:
        https://github.com/facebook/react/pull/123

    Example output:
        ("facebook", "react", 123)
    """
    pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.search(pattern, pr_url)

    if not match:
        raise ValueError(f"Invalid GitHub PR URL: {pr_url}")

    owner, repo, pr_number = match.groups()
    return owner, repo, int(pr_number)


async def fetch_pr_data(pr_url: str) -> dict:
    """
    Calls the GitHub API twice:
    1. Get PR info (title, author, branches)
    2. Get changed files with diffs
    """
    owner, repo, pr_number = parse_pr_url(pr_url)

    # This is our "library card" - proves who we are to GitHub
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:

        # First API call — get PR metadata
        meta_resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=headers,
        )
        meta_resp.raise_for_status()
        pr_meta = meta_resp.json()

        # Second API call — get changed files
        files_resp = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files",
            headers=headers,
            params={"per_page": 50},
        )
        files_resp.raise_for_status()
        pr_files = files_resp.json()

    # Package everything into one clean dictionary
    return {
        "title": pr_meta["title"],
        "description": pr_meta.get("body") or "No description provided.",
        "author": pr_meta["user"]["login"],
        "base_branch": pr_meta["base"]["ref"],
        "head_branch": pr_meta["head"]["ref"],
        "files": [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f["additions"],
                "deletions": f["deletions"],
                "patch": f.get("patch", ""),
            }
            for f in pr_files
            if f.get("patch")   # skip binary files — they have no text diff
        ],
    }