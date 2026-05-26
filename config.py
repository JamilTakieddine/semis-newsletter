import os
from dataclasses import dataclass


@dataclass
class Config:
    anthropic_api_key: str
    gmail_sender: str
    gmail_app_password: str
    recipient_email: str


def load_config() -> Config:
    required = {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GMAIL_SENDER": os.getenv("GMAIL_SENDER"),
        "GMAIL_APP_PASSWORD": os.getenv("GMAIL_APP_PASSWORD"),
        "RECIPIENT_EMAIL": os.getenv("RECIPIENT_EMAIL"),
    }

    missing = [k for k, v in required.items() if not v]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return Config(
        anthropic_api_key=required["ANTHROPIC_API_KEY"],
        gmail_sender=required["GMAIL_SENDER"],
        gmail_app_password=required["GMAIL_APP_PASSWORD"],
        recipient_email=required["RECIPIENT_EMAIL"],
    )