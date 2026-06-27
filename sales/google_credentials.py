import os
from pathlib import Path
from django.conf import settings


def ensure_google_credentials():
    """
    Creates credentials.json and token.json from
    Render environment variables if they don't exist.
    """

    credentials_dir = Path(settings.BASE_DIR) / "credentials"
    credentials_dir.mkdir(exist_ok=True)

    credentials_file = credentials_dir / "credentials.json"
    token_file = credentials_dir / "token.json"

    credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    token_json = os.environ.get("GOOGLE_TOKEN_JSON")

    if credentials_json and not credentials_file.exists():
        credentials_file.write_text(credentials_json, encoding="utf-8")

    if token_json and not token_file.exists():
        token_file.write_text(token_json, encoding="utf-8")