import click
import os
from pathlib import Path
import requests
from shield.core import load_config

@click.command()
def test():
    """Run a test to verify config, webhook, and log file setup."""
    config = load_config()
    webhook_url = config.get("webhook_url")
    logfile = "/var/log/auth.log"
    errors = []

    click.echo("🧪 Running MinakiShield system test...\n")

    if not webhook_url:
        errors.append("❌ Missing `webhook_url` in ~/.minakishield/config.yaml")
    else:
        click.echo("📡 Found webhook URL.")
        try:
            test_payload = {
                "text": "🛡️ *MinakiShield Test Alert*: Everything is working!"
            }
            r = requests.post(webhook_url, json=test_payload, timeout=3)
            if r.status_code == 200:
                click.echo("✅ Webhook test sent successfully.")
            else:
                errors.append(f"❌ Webhook returned status {r.status_code}")
        except Exception as e:
            errors.append(f"❌ Webhook error: {e}")

    if os.path.exists(logfile):
        click.echo(f"📁 Log file exists: {logfile}")
    else:
        errors.append(f"❌ Log file not found: {logfile}")

    if errors:
        click.echo("\n❌ Some checks failed:")
        for err in errors:
            click.echo(f"   {err}")
        exit(1)
    else:
        click.echo("\n✅ All systems are GO!")
