from fastapi import APIRouter, HTTPException
from models.schemas import ReviewRequest, ReviewResponse
from services.github import fetch_pr_data
from services.reviewer import run_review



router = APIRouter(prefix="/api", tags=["review"])


@router.post("/review", response_model=ReviewResponse)
async def review_pull_request(request: ReviewRequest):
    """
    Main endpoint — receives PR URL, runs full AI review,
    returns structured results.

    Flow:
    Request → fetch from GitHub → run AI review → return results
    """

    # Fetch PR data from GitHub
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

    # Check there are actually reviewable files
    if not pr_data["files"]:
        raise HTTPException(
            status_code=422,
            detail="No reviewable file changes found in this PR.",
        )

    # Run the AI review
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
