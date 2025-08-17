from app.deps import verify_signature
import hmac, hashlib

def test_verify_signature_ok():
    secret = "s3cr3t"
    body = b'{"ok":true}'
    sig="sha256="+ hmac.new(secret.encode(),body, hashlib.sha256).hexdigest()
    verify_signature(body, sig)