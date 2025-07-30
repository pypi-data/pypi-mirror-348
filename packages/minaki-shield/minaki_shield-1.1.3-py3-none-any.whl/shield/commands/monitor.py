import click
import os
import subprocess
import sys
from shield.core import load_services, monitor_logs

@click.command()
@click.option('--logfile', '-l', multiple=True, help='Path to log file(s)', required=True)
@click.option('--log-to-file', is_flag=True, default=False, help='Log alerts to ~/.minakishield/shield.log')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Output alerts in JSON format')
@click.option('--webhook-url', type=str, help='Send alerts to a webhook (e.g. Slack)')
@click.option('--daemon', is_flag=True, default=False, help='Run in background as a daemon')
def monitor(logfile, log_to_file, json_output, webhook_url, daemon):
    """Monitor log files for suspicious activity."""
    if daemon:
        args = [
            sys.executable, '-m', 'shield.cli', 'monitor',
            *[arg for path in logfile for arg in ('--logfile', path)],
        ]
        if log_to_file:
            args.append('--log-to-file')
        if json_output:
            args.append('--json')
        if webhook_url:
            args.extend(['--webhook-url', webhook_url])

        pidfile = os.path.expanduser('~/.minakishield/shield.pid')
        logdir = os.path.dirname(pidfile)
        os.makedirs(logdir, exist_ok=True)

        with open(pidfile, 'w') as f:
            proc = subprocess.Popen(args)
            f.write(str(proc.pid))

        click.echo(f"🚀 Shield is now running in the background (PID {proc.pid})")
        click.echo(f"📝 PID written to {pidfile}")
        return

    click.echo("🧠 Loading internal detection services...")
    services = load_services()

    click.echo(f"👁️ Watching {', '.join(logfile)}")
    monitor_logs(
        logfile,
        services,
        log_to_file=log_to_file,
        json_output=json_output,
        webhook_url=webhook_url
    )
