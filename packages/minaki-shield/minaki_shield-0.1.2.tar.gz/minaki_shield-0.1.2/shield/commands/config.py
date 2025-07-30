import click
from pathlib import Path
import yaml
import os

CONFIG_PATH = Path.home() / ".minakishield" / "config.yaml"

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
        config_data = {"webhook_url": set_webhook}
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(config_data, f)
        click.echo(f"✅ Webhook updated and saved to {CONFIG_PATH}")
        return

    # Default behavior if no flag is used
    click.echo("ℹ️ Use one of the options:")
    click.echo("   --show           Show current config")
    click.echo("   --set-webhook    Provide a new webhook URL")
    click.echo("   --reset          Delete the config file")
