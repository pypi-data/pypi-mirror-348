import click
from pathlib import Path

@click.command()
@click.option('--tail', '-n', default=20, help='Number of lines to show from the end of the log.')
def logs(tail):
    """View recent Shield alerts from the log file."""
    log_path = Path.home() / ".minakishield" / "shield.log"

    if not log_path.exists():
        click.echo("⚠️  No log file found. Has Shield run yet?")
        return

    with open(log_path, 'r') as f:
        lines = f.readlines()

    click.echo(f"📄 Showing last {min(tail, len(lines))} log entries:\n")
    for line in lines[-tail:]:
        click.echo(line.strip())
