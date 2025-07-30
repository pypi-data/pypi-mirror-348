import click
from pathlib import Path
import yaml

CONFIG_PATH = Path("/etc/minaki/config.yaml")

@click.command()
def setup():
    """Interactive setup for MinakiShield webhook config."""
    click.echo("🛡️  Welcome to MinakiShield Setup")

    webhook_url = click.prompt("🔗 Enter your Slack webhook URL", type=str)

    # Load existing config if present
    config_data = {}
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                config_data = yaml.safe_load(f) or {}
        except Exception as e:
            click.echo(f"⚠️ Failed to load existing config: {e}")
            config_data = {}

    # Update the webhook URL and ensure logfiles are present
    config_data["webhook_url"] = webhook_url
    config_data.setdefault("logfiles", ["/var/log/auth.log"])

    # Ensure directory exists
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save updated config
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config_data, f, default_flow_style=False)

    click.echo(f"✅ Webhook saved to {CONFIG_PATH}")
    click.echo("📦 This config will now be used by MinakiShield automatically.")
