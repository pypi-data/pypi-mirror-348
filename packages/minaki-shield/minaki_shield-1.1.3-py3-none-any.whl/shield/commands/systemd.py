import click
import os
import subprocess
from pathlib import Path

@click.command()
@click.option('--logfile', default='/var/log/auth.log', help='Log file to monitor')
@click.option('--log-to-file', is_flag=True, help='Enable logging to /etc/minaki/shield.log')
@click.option('--json', 'json_output', is_flag=True, help='Output alerts as JSON')
@click.option('--webhook-url', help='Webhook URL for alerts (e.g., Slack)')
def systemd(logfile, log_to_file, json_output, webhook_url):
    """Generate and activate a systemd service for MinakiShield (system-level only)."""

    # Systemd service install path
    config_dir = Path("/etc/systemd/system")
    service_path = config_dir / "minakishield.service"

    # System executable path
    shield_exec = "/usr/bin/shield"

    # Ensure /etc/minaki exists
    etc_minaki = Path("/etc/minaki")
    etc_minaki.mkdir(parents=True, exist_ok=True)

    # Build ExecStart args
    args = f"--logfile {logfile}"
    if log_to_file:
        args += " --log-to-file"
    if json_output:
        args += " --json"
    if webhook_url:
        args += f" --webhook-url {webhook_url}"

    log_path = "/etc/minaki/shield.log"
    working_dir = "/etc/minaki"

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
WantedBy=multi-user.target
"""

#    try:
#        with open(service_path, 'w') as f:
#            f.write(service_content)
#        click.echo(f"✅ Systemd service created at: {service_path}")
#    except Exception as e:
#        click.echo(f"❌ Error writing systemd service file: {e}")
#        return

    try:
        import tempfile
        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            tmp.write(service_content)
            tmp_path = tmp.name

        subprocess.run(["sudo", "cp", tmp_path, str(service_path)], check=True)
        os.unlink(tmp_path)
        click.echo(f"✅ Systemd service created at: {service_path}")
    except Exception as e:
        click.echo(f"❌ Error writing systemd service file: {e}")
        return

    try:
        subprocess.run(["sudo", "systemctl", "daemon-reexec"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "--now", "minakishield.service"], check=True)
        click.echo("🚀 MinakiShield system service enabled and started!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start service: {e}")

    try:
        subprocess.run(["sudo", "systemctl", "daemon-reexec"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "--now", "minakishield.service"], check=True)
        click.echo("🚀 MinakiShield system service enabled and started!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start service: {e}")
