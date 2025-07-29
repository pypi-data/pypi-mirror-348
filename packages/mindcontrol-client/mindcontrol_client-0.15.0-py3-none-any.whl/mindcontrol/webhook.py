import hmac
import hashlib
import base64
from typing import Optional
from mindcontrol_types import WebhookV1


def verify_webhook(body: str, secret: str, signature: str) -> bool:
    """Verifies a webhook body using the webhook secret and signature.

    :param body: Raw body string to verify.
    :param secret: Webhook secret to verify the signature.
    :param signature: Signature to verify the body.

    :return: True if the signature is valid, False otherwise."""

    computed_signature = hmac.new(
        secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).digest()
    signature_bytes = base64.b64decode(signature)

    return hmac.compare_digest(computed_signature, signature_bytes)


def parse_webhook(body: str, secret: str, signature: str) -> Optional[WebhookV1]:
    """Parses a webhook body and verifies its signature.

    :param body: Raw body string to verify and parse.
    :param secret: Webhook secret to verify the signature.
    :param signature: Signature to verify the body.

    :return: Parsed webhook object or None if verification failed."""

    if not verify_webhook(body, secret, signature):
        return None

    return WebhookV1.model_validate_json(body)
