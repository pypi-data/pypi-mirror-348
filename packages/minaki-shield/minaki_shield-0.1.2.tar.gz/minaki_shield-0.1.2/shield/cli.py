import click
import importlib.metadata

# Import core commands
from shield.commands import monitor, stop, status, systemd, restart
from shield.commands import services as services_cmd
from shield.commands import logs as logs_cmd
from shield.commands.setup import setup
from shield.commands.config import config
from shield.commands.test import test
from shield.commands.os_plugins import os_plugins  # Plugin management commands
from shield.commands.uninstall import uninstall

# Import plugin handling from core
from shield.core import load_plugins

@click.group()
@click.version_option(importlib.metadata.version("minaki-shield"))
def main():
    """🛡️ MinakiLabs Shield - Linux intrusion detection CLI."""
    pass

# Register core CLI subcommands
main.add_command(monitor.monitor)
main.add_command(stop.stop)
main.add_command(status.status)
main.add_command(systemd.systemd)
main.add_command(restart.restart)
main.add_command(services_cmd.services)
main.add_command(logs_cmd.logs)
main.add_command(setup)
main.add_command(config)
main.add_command(test)
main.add_command(uninstall)

# Plugin command group for managing and running plugins
@click.group(help="Manage user-installed plugins.")
def plugins():
    """Plugin management and execution."""
    pass

# Add plugin management commands directly to the plugins group
plugins.add_command(os_plugins, name="manage")

# Plugin run command group
@click.group(name="run", help="Run a user-installed plugin.")
def run():
    """Run user-installed plugins."""
    pass

# Dynamically load and add plugins as subcommands under "plugins run"
loaded_plugins = load_plugins()
for plugin_name, plugin_func in loaded_plugins:
    run.add_command(plugin_func, name=plugin_name)

# Add the "run" command group to plugins
plugins.add_command(run, name="run")

# Add the plugins command group to the main CLI
main.add_command(plugins, name="plugins")

if __name__ == '__main__':
    main()
