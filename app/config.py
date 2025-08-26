from pydantic import BaseModel
import os, base64
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):

    port: int = int(os.getenv("PORT", "3000"))
    app_id: str = os.environ["GITHUB_APP_ID"]
    installation_id: str = os.environ["GITHUB_INSTALLATION_ID"]
    webhook_secret: str = os.environ["GITHUB_WEBHOOK_SECRET"]
    private_key_pem: str = base64.b64decode(os.environ["GITHUB_PRIVATE_KEY_BASE64"]).decode("utf-8")
    open_ai_key: str = os.environ["OPENAI_API_KEY"]
    openai_model: str = os.getenv("OPENAI_MODEL","gpt-4o-mini")
    review_max_files: int = int(os.getenv("REVIEW_MAX_FILE","30"))
    review_max_patch_chars: int = int(os.getenv("REVIEW_MAX_PATCH_CHARS",60000))
    gitlab_token: str = os.environ["GITLAB_TOKEN"]
    gemini_key: str = os.environ["GEMINI_API_KEY"]
    gemini_model: str = os.environ["GEMINI_MODEL"]

settings = Settings()