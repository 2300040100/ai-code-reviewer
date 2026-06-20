# AI Code Reviewer

An AI-powered GitHub Pull Request reviewer built with FastAPI, React, and Groq AI.

Paste any public GitHub PR URL and get an instant structured code review covering bugs, security vulnerabilities, performance issues, and code style — each with severity levels and concrete fix suggestions.

![Built With](https://img.shields.io/badge/Built%20With-FastAPI%20%7C%20React%20%7C%20Groq%20AI-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Bug Detection — logic errors, null pointer risks, race conditions
- Performance Issues — N+1 queries, memory leaks, inefficient algorithms
- Security Vulnerabilities — SQL injection, XSS, hardcoded secrets
- Code Style — naming conventions, SOLID/DRY violations, dead code
- Dark/Light mode toggle
- PR Stats — author, files reviewed, additions/deletions
- Filter by category and severity
- Copy review as Markdown report
- Mobile responsive layout
- Handles large PRs — auto-chunks 100+ file PRs

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Frontend | React 18, Vite |
| AI Model | Groq API (LLaMA 3.3 70B) |
| GitHub Integration | GitHub REST API v3 |
| Validation | Pydantic v2 |
| HTTP Client | httpx (async) |
| Deployment | Railway (backend) + Vercel (frontend) |

## Architecture

```
User → React Frontend → FastAPI Backend → GitHub API (fetch PR diff)
→ Groq AI (analyze code)
→ Structured JSON Response
```

## Running Locally

### Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API key (free at console.groq.com)
- GitHub Personal Access Token

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Create `backend/.env`:

```
OPENAI_API_KEY=gsk_your_groq_key
GITHUB_TOKEN=ghp_your_github_token
OPENAI_MODEL=llama-3.3-70b-versatile
MAX_TOKENS=2048
```

```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Documentation

After starting the backend, visit http://localhost:8000/docs for interactive Swagger UI.

### POST /api/review

Request:

```json
{
  "pr_url": "https://github.com/owner/repo/pull/123",
  "focus_areas": ["bugs", "performance", "style", "security"]
}
```

Response:

```json
{
  "pr_title": "Fix authentication flow",
  "pr_url": "https://github.com/owner/repo/pull/123",
  "stats": {
    "author": "developer",
    "files_reviewed": 5,
    "total_additions": 120,
    "total_deletions": 45
  },
  "issues": [
    {
      "category": "security",
      "severity": "critical",
      "file": "auth/login.py",
      "line": "34",
      "title": "Hardcoded secret key",
      "description": "SECRET_KEY is hardcoded in source code",
      "suggestion": "Move to environment variable using os.getenv()"
    }
  ],
  "summary": {
    "total_issues": 4,
    "critical": 1,
    "high": 1,
    "medium": 1,
    "low": 1,
    "overall_assessment": "..."
  }
}
```

## Project Structure

```
ai-code-reviewer/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Settings from .env
│   ├── models/
│   │   └── schemas.py           # Pydantic data models
│   ├── routers/
│   │   └── review.py            # POST /api/review endpoint
│   └── services/
│       ├── github.py            # GitHub API integration
│       ├── prompt.py            # AI prompt builder
│       └── reviewer.py          # Groq AI orchestration
└── frontend/
    └── src/
        ├── App.jsx              # Root component
        ├── components/
        │   ├── PRInput.jsx      # URL input form
        │   ├── SummaryBar.jsx   # Review summary
        │   └── ReviewCard.jsx   # Issue cards
        └── services/
            └── api.js           # Backend API calls
```

## Planned Features

- Review history with SQLite database
- GitHub OAuth authentication
- Streaming AI responses
- GitHub webhook — auto-review on PR open
- Post review comments directly to GitHub PR
- GitLab and Bitbucket support
- Unit tests with pytest + Vitest

## Author

Designed, built, and deployed with ❤️

---

If you found this useful, give it a star on GitHub.
