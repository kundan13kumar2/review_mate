import uvicorn
from fastapi import FastAPI
from .config import settings
from .webhook import router as webhook_router

app = FastAPI(title="AI PR Reviewer (FastAPI)")
app.include_router(webhook_router)

def run():
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)


if __name__ == "__main__":
    run()