import click
import subprocess
import os

@click.command()
def stop():
    """Stop Shield systemd service."""
    is_system_scope = os.path.exists("/etc/systemd/system/minakishield.service")

    try:
        if is_system_scope:
            subprocess.run(["sudo", "systemctl", "stop", "minakishield.service"], check=True)
        else:
            subprocess.run(["systemctl", "--user", "stop", "minakishield.service"], check=True)

        click.echo("🛑 Shield service stopped via systemd.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to stop Shield. Is it installed?")
