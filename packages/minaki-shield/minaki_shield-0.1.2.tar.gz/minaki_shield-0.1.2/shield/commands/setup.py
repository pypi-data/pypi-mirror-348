import click
from pathlib import Path
import yaml

CONFIG_PATH = Path.home() / ".minakishield" / "config.yaml"

@click.command()
def setup():
    """Interactive setup for MinakiShield webhook config."""
    click.echo("🛡️  Welcome to MinakiShield Setup")
    
    webhook_url = click.prompt("🔗 Enter your Slack webhook URL", type=str)

    # Create directory if needed
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write config
    config_data = {"webhook_url": webhook_url}
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config_data, f)

    click.echo(f"✅ Webhook saved to {CONFIG_PATH}")
    click.echo("📦 This will now be used automatically unless overridden by CLI")
