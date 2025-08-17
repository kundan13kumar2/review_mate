from fastapi import APIRouter, Request, Response, Depends
from .deps import verify_signature, github_headers
from .review_service import review_pull_request

router = APIRouter(prefix="/api")

@router.get("/first")
async def firstTest():
    return {"message":"Hello"}


@router.post("/webhook")
async def webhook(req:Request, res: Response, hdrs=Depends(github_headers)):
    event,sig = hdrs
    raw = await req.body()
    verify_signature(raw, sig)

    payload = await req.json()

    if event == "pull_request" and payload.get("action") in {"opened","synchronize","ready_for_review","reopened"}:
        repo = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        import asyncio
        asyncio.create_task(review_pull_request(repo, pr_number))
    
    return {"ok": True}
