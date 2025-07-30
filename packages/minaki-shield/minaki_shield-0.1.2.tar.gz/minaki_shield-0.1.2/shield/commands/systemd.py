import click
import os
import subprocess
from pathlib import Path

@click.command()
@click.option('--logfile', default='/var/log/auth.log', help='Log file to monitor')
@click.option('--log-to-file', is_flag=True, help='Enable logging to ~/.minakishield/shield.log')
@click.option('--json', 'json_output', is_flag=True, help='Output alerts as JSON')
@click.option('--webhook-url', help='Webhook URL for alerts (e.g., Slack)')
@click.option('--scope', type=click.Choice(['user', 'system']), default='user', help='Install service at user or system level')
def systemd(logfile, log_to_file, json_output, webhook_url, scope):
    """Generate and activate a systemd service for Shield."""

    if scope == 'system':
        config_dir = Path("/etc/systemd/system")
        shield_exec = "/usr/local/bin/shield"
        reload_cmd = ["sudo", "systemctl", "daemon-reexec"]
        enable_cmd = ["sudo", "systemctl", "enable", "--now", "minakishield.service"]
    else:
        config_dir = Path.home() / ".config/systemd/user"
        shield_exec = os.path.expanduser("~/.local/bin/shield")
        reload_cmd = ["systemctl", "--user", "daemon-reload"]
        enable_cmd = ["systemctl", "--user", "enable", "--now", "minakishield.service"]

    config_dir.mkdir(parents=True, exist_ok=True)

    args = f"--logfile {logfile}"
    if log_to_file:
        args += " --log-to-file"
    if json_output:
        args += " --json"
    if webhook_url:
        args += f" --webhook-url {webhook_url}"

    log_path = Path.home() / ".minakishield" / "shield.log"
    working_dir = Path.home() / ".minakishield"

    service_content = f"""[Unit]
Description=MinakiLabs Shield Intrusion Detection
After=network.target

[Service]
ExecStart={shield_exec} monitor {args}
WorkingDirectory={working_dir}
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=5
StandardOutput=append:{log_path}
StandardError=append:{log_path}

[Install]
WantedBy=default.target
"""

    service_path = config_dir / "minakishield.service"

    try:
        with open(service_path, 'w') as f:
            f.write(service_content)
        click.echo(f"✅ Systemd service created at: {service_path}")
    except Exception as e:
        click.echo(f"❌ Error writing service file: {e}")
        return

    try:
        subprocess.run(reload_cmd, check=True)
        subprocess.run(enable_cmd, check=True)
        click.echo("🚀 MinakiShield service enabled and started!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start service: {e}")
