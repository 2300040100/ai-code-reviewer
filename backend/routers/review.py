from fastapi import APIRouter, HTTPException
from models.schemas import ReviewRequest, ReviewResponse
from services.github import fetch_pr_data
from services.reviewer import run_review


# APIRouter is like a mini FastAPI app
# prefix="/api" means all routes here start with /api
router = APIRouter(prefix="/api", tags=["review"])


@router.post("/review", response_model=ReviewResponse)
async def review_pull_request(request: ReviewRequest):
    """
    Main endpoint — receives PR URL, runs full AI review,
    returns structured results.

    Flow:
    Request → fetch from GitHub → run AI review → return results
    """

    # Step 1 — Fetch PR data from GitHub
    try:
        pr_data = await fetch_pr_data(request.pr_url)
    except ValueError as e:
        # This fires if the URL format is wrong
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # This fires if GitHub API fails (network error, bad token etc)
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch PR from GitHub: {str(e)}",
        )

    # Step 2 — Check there are actually reviewable files
    if not pr_data["files"]:
        raise HTTPException(
            status_code=422,
            detail="No reviewable file changes found in this PR.",
        )

    # Step 3 — Run the AI review
    try:
        result = await run_review(
            request.pr_url,
            pr_data,
            request.focus_areas,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI review failed: {str(e)}",
        )

    return result