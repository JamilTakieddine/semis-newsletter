import sys
from config import load_config
from newsletter import generate_newsletter
from emailer import send_email


def main():
    print("Starting Semiconductor Daily Briefing agent...")

    # 1. Load and validate all config
    config = load_config()
    print("✓ Config loaded")

    # 2. Call Claude with web search — returns formatted HTML
    print("Searching for today's semiconductor news...")
    html = generate_newsletter(api_key=config.anthropic_api_key)
    print(f"✓ Newsletter generated ({len(html)} chars)")

    # 3. Send via Gmail SMTP
    send_email(
        sender=config.gmail_sender,
        app_password=config.gmail_app_password,
        recipient=config.recipient_email,
        html_body=html,
    )

    print("✓ Done. Exiting.")
    sys.exit(0)


if __name__ == "__main__":
    main()