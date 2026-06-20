from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.review import router

app = FastAPI(
    title="AI Code Reviewer",
    description="Automated pull request review using OpenAI GPT",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect our review router to the main app
app.include_router(router)


@app.get("/")
def root():
    return {"message": "AI Code Reviewer is running!"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
