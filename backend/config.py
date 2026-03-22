from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  openai_api_key: str
  github_token: str
  openai_model: str = "gpt-4o"
  max_tokens: int = 4096


  class Config:
    env_file = ".env"

settings = Settings()