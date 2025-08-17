from sre_parse import ANY
import time, jwt, httpx
from typing import Any, Dict, List
from .config import settings

GITHUB_API = "https://api.github.com"

def _app_jwt() -> str:
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + 9*60,
        "iss": int(settings.app_id)
    }
    return jwt.encode(payload, settings.private_key_pem, algorithm="RS256")

async def _installation_token() -> str:
    async with httpx.AsyncClient(base_url=GITHUB_API, headers={"Accept":"application/vnd.github+json"}) as client:
        jwt_token = _app_jwt()
        r = await client.post(
            f"/app/installations/{settings.installation_id}/access_tokens",
            headers={"Authorization":f"Bearer {jwt_token}"},
        )
        r.raise_for_status()
        return r.json()["token"]

async def _authed() -> httpx.AsyncClient:
    token = await _installation_token()
    return httpx.AsyncClient(
        base_url=GITHUB_API,
        headers={"Authorization":f"Bearer {token}", "Accept":"application/vnd.github+json"},
    )

async def get_pr_metadata(owner: str, repo: str, number: int) -> Dict[str, any]:
    metadata: Dict[str, Any] = []
    async with await _authed() as client:
        r = await client.get(f"/repos/{owner}/{repo}/pulls/{number}")
        r.raise_for_status()
        metadata = r.json()
    return metadata    


async def list_pr_files(owner: str, repo: str, number: int) -> List[Dict[str, Any]]:
    files: List[Dict[str, Any]] = []
    page = 1 
    async with await _authed() as client:
        while True:
            r = await client.get(f"/repos/{owner}/{repo}/pulls/{number}/files", params={"per_page":100, "page":page})
            r.raise_for_status()
            batch = r.json()
            files.extend(batch)
            if len(batch) < 100: break
            page += 1
    return files

async def create_review(owner: str, repo: str, number: int, body: str, comments: list[dict]):
    async with await _authed() as client:
        payload = {
            "event": "COMMENT",
            "body": '',
            "comments": [ {**c, "side":"RIGHT"} for c in comments],
        }

        r = await client.post(f"/repos/{owner}/{repo}/pulls/{number}/reviews", json=payload)
        r.raise_for_status()
        return r.json()