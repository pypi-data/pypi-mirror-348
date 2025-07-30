import click
import subprocess
import os

@click.command()
def stop():
    """Stop Shield systemd service."""
    is_system_scope = os.path.exists("/etc/systemd/system/minakishield.service")
    base_cmd = ["systemctl"]
    if not is_system_scope:
        base_cmd.append("--user")

    try:
        subprocess.run(base_cmd + ["stop", "minakishield.service"], check=True)
        click.echo("🛑 Shield service stopped via systemd.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to stop Shield. Is it installed?")
