import click
import subprocess
import os

@click.command()
def restart():
    """Restart Shield systemd service."""

    # Check both system and user scope
    system_unit = "/etc/systemd/system/minakishield.service"
    user_unit = os.path.expanduser("~/.config/systemd/user/minakishield.service")

    # Determine where the unit is installed
    if os.path.exists(system_unit):
        scope = "system"
    elif os.path.exists(user_unit):
        scope = "user"
    else:
        click.echo("❌ MinakiShield service not found in system or user scope.")
        return

    # Build the command
    base_cmd = ["systemctl"]
    if scope == "user":
        base_cmd.append("--user")

    # Always allow systemctl to handle the privilege escalation (e.g. via polkit)
    try:
        subprocess.run(base_cmd + ["restart", "minakishield.service"], check=True)
        click.echo("🔁 Shield service restarted.")
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to restart Shield.")
