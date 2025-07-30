import click
import subprocess
import os

@click.command()
def status():
    """Check if Shield is currently running via systemd."""

    is_system_scope = os.path.exists("/etc/systemd/system/minakishield.service")
    base_cmd = ["systemctl"]
    if not is_system_scope:
        base_cmd.append("--user")

    try:
        output = subprocess.check_output(
            base_cmd + ["is-active", "minakishield.service"],
            stderr=subprocess.STDOUT
        ).decode().strip()

        if output == "active":
            click.echo("✅ Shield is running (via systemd)")
        elif output == "inactive":
            click.echo("🛑 Shield is installed but not running.")
        elif output == "failed":
            click.echo("❌ Shield service failed (check journalctl)")
        else:
            click.echo(f"⚠️ Shield status: {output}")
    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode().strip() if e.output else "Unknown error"
        if "could not be found" in error_msg:
            click.echo("❌ Shield systemd service not found.")
        else:
            click.echo(f"❌ Could not determine Shield status: {error_msg}")
