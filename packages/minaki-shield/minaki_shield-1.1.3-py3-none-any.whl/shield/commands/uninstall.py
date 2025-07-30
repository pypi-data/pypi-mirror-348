import click
import os
import subprocess
from pathlib import Path

@click.command()
def uninstall():
    """Uninstall MinakiShield systemd service and stop monitoring."""

    service_path = "/etc/systemd/system/minakishield.service"
    disable_cmd = ["sudo", "systemctl", "disable", "--now", "minakishield.service"]
    reload_cmd = ["sudo", "systemctl", "daemon-reexec"]

    click.echo("🛑 Stopping any running MinakiShield services...")

    try:
        subprocess.run(disable_cmd, check=True)
    except subprocess.CalledProcessError:
        click.echo("⚠️  Could not stop or disable the service.")

    if os.path.exists(service_path):
        try:
            subprocess.run(["sudo", "rm", service_path], check=True)
            click.echo("🧹 Service file removed.")
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Failed to remove service file: {e}")
    else:
        click.echo("ℹ️ No service file found to remove.")

    subprocess.run(reload_cmd, check=True)
    click.echo("✅ MinakiShield systemd service has been fully uninstalled.")
