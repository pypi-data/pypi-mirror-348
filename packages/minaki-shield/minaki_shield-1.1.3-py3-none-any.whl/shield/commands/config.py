import click
from pathlib import Path
import yaml
import os

CONFIG_PATH = Path("/etc/minaki/config.yaml")

@click.command()
@click.option('--show', is_flag=True, help='Display the current config.yaml contents.')
@click.option('--set-webhook', prompt=False, help='Set or update the Slack webhook URL.')
@click.option('--reset', is_flag=True, help='Delete config.yaml and start fresh.')
def config(show, set_webhook, reset):
    """Manage your MinakiShield config.yaml file."""

    if reset:
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
            click.echo("🔄 config.yaml has been deleted.")
        else:
            click.echo("⚠️ No config.yaml to delete.")
        return

    if show:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r') as f:
                content = f.read()
            click.echo("📄 Current config.yaml contents:\n")
            click.echo(click.style(content, fg='green'))
        else:
            click.echo("⚠️ config.yaml not found.")
        return

    if set_webhook:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        config_data = {}

        # Load existing config if available
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
            except Exception as e:
                click.echo(f"⚠️ Failed to load existing config: {e}")
                config_data = {}

        # Update webhook_url
        config_data['webhook_url'] = set_webhook

        # Ensure logfiles key exists
        config_data.setdefault('logfiles', ["/var/log/auth.log"])

        # Save updated config
        with open(CONFIG_PATH, 'w') as f:
            yaml.safe_dump(config_data, f, default_flow_style=False)

        click.echo(f"✅ Webhook updated and saved to {CONFIG_PATH}")
        return

    # Default help if no option
    click.echo("ℹ️ Use one of the options:")
    click.echo("   --show           Show current config")
    click.echo("   --set-webhook    Provide a new webhook URL")
    click.echo("   --reset          Delete the config file")
