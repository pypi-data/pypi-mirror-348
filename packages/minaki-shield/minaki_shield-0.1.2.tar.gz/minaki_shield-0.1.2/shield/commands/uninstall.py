import click
import os
import subprocess
from pathlib import Path

@click.command()
@click.option('--scope', type=click.Choice(['user', 'system']), default='user', help='Uninstall service at user or system level')
def uninstall(scope):
    """Uninstall MinakiShield systemd service and stop monitoring."""

    if scope == 'system':
        service_path = "/etc/systemd/system/minakishield.service"
        disable_cmd = ["sudo", "systemctl", "disable", "--now", "minakishield.service"]
        reload_cmd = ["sudo", "systemctl", "daemon-reexec"]
    else:
        service_path = Path.home() / ".config/systemd/user/minakishield.service"
        disable_cmd = ["systemctl", "--user", "disable", "--now", "minakishield.service"]
        reload_cmd = ["systemctl", "--user", "daemon-reload"]

    click.echo("🛑 Stopping any running MinakiShield services...")

    try:
        subprocess.run(disable_cmd, check=True)
    except subprocess.CalledProcessError:
        click.echo("⚠️  Could not stop or disable the service.")

    if os.path.exists(service_path):
        try:
            os.remove(service_path)
            click.echo("🧹 Service file removed.")
        except Exception as e:
            click.echo(f"❌ Failed to remove service file: {e}")
    else:
        click.echo("ℹ️ No service file found to remove.")

    subprocess.run(reload_cmd, check=True)
    click.echo("✅ MinakiShield systemd services have been uninstalled.")
