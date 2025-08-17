import hmac, hashlib
from fastapi import Header, HTTPException
from .config import settings

def verify_signature(raw_body: bytes, signature_256: str | None):

    if not signature_256:
        raise HTTPException(status_code=401, detail="Missing Signature")

        mac = hmac.new(settings.webhook_secret.encode(), msg= raw_body, digestmod=hashlib.sha256)
        expected = "sha256=" + mac.hexdigest()
        if not hmac.compare_digest(expected, signature_256):
            raise HTTPException(status_code=401, detail="Invalid Signature")

async def github_headers(
    gh_event: str = Header(..., alias="X-GitHub-Event"),
    gh_sig: str = Header(..., alias= "X-Hub-Signature-256")
): return gh_event, gh_sig
