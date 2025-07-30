import click
import subprocess
import os

@click.command()
def restart():
    """Restart MinakiShield systemd service (system-level only)."""

    system_unit = "/etc/systemd/system/minakishield.service"

    if not os.path.exists(system_unit):
        click.echo("❌ MinakiShield system service not found.")
        return

    try:
        subprocess.run(["sudo", "systemctl", "restart", "minakishield.service"], check=True)
        click.echo("🔁 MinakiShield system service restarted successfully.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to restart MinakiShield system service.")
