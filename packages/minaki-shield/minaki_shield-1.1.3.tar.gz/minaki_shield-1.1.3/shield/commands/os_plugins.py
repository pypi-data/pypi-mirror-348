import click
import os
import requests
from pathlib import Path

PLUGIN_API_URL = "https://api.github.com/repos/MinakiLabs-Official/minaki-shield-plugins/contents/plugins"
PLUGIN_RAW_URL = "https://raw.githubusercontent.com/MinakiLabs-Official/minaki-shield-plugins/main/plugins"

@click.group()
def os_plugins():
    """Manage OS-related MinakiShield plugins."""
    pass

@os_plugins.command()
@click.argument("plugin_name")
def install(plugin_name):
    """Install a plugin from the public repo."""
    plugin_dir = Path.home() / ".minakishield" / "plugins"
    plugin_dir.mkdir(parents=True, exist_ok=True)

    url = f"{PLUGIN_RAW_URL}/{plugin_name}.py"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(plugin_dir / f"{plugin_name}.py", "w") as f:
                f.write(response.text)
            click.echo(f"✅ Installed plugin: {plugin_name}")
        else:
            click.echo(f"❌ Failed to install plugin '{plugin_name}': {response.status_code} Not Found")
    except Exception as e:
        click.echo(f"⚠️ Error installing plugin: {e}")

@os_plugins.command()
def list():
    """List all installed plugins."""
    plugin_dir = Path.home() / ".minakishield" / "plugins"
    if not plugin_dir.exists():
        click.echo("🛑 No plugins installed.")
        return

    plugins = [f.stem for f in plugin_dir.glob("*.py")]
    if plugins:
        click.echo("🧩 Installed plugins:")
        for plugin in plugins:
            click.echo(f"  ✅ {plugin}")
    else:
        click.echo("🛑 No plugins installed.")

@os_plugins.command()
def list_available():
    """List all plugins available from the public repo."""
    try:
        response = requests.get(PLUGIN_API_URL)
        if response.status_code == 200:
            plugins = [file['name'].replace('.py', '') for file in response.json() if file['name'].endswith('.py')]
            click.echo("🌐 Available plugins from public repo:")
            for plugin in plugins:
                click.echo(f"  ✅ {plugin}")
        else:
            click.echo("❌ Failed to fetch plugin list from the public repo.")
    except Exception as e:
        click.echo(f"⚠️ Error fetching plugins: {e}")

@os_plugins.command()
def check_updates():
    """Check if any installed plugins need an update."""
    plugin_dir = Path.home() / ".minakishield" / "plugins"
    if not plugin_dir.exists():
        click.echo("🛑 No plugins installed locally.")
        return

    local_plugins = {f.stem: f for f in plugin_dir.glob("*.py")}
    try:
        response = requests.get(PLUGIN_API_URL)
        if response.status_code == 200:
            available_plugins = [file['name'].replace('.py', '') for file in response.json() if file['name'].endswith('.py')]
            click.echo("🔄 Checking for updates:")
            for plugin in available_plugins:
                if plugin in local_plugins:
                    local_version = local_plugins[plugin].stat().st_mtime
                    remote_url = f"{PLUGIN_RAW_URL}/{plugin}.py"
                    remote_response = requests.get(remote_url)
                    if remote_response.status_code == 200:
                        remote_version = remote_response.headers.get('Last-Modified', 'Unknown')
                        click.echo(f"  🔍 {plugin}: Local version timestamp: {local_version}, Remote version: {remote_version}")
                    else:
                        click.echo(f"❌ Failed to fetch version for {plugin}")
                else:
                    click.echo(f"  ❗ {plugin} not installed locally.")
        else:
            click.echo("❌ Failed to fetch plugin list from the public repo.")
    except Exception as e:
        click.echo(f"⚠️ Error checking updates: {e}")

@os_plugins.command(name="uninstall", help="Uninstall a plugin.")
@click.argument("plugin_name")
def uninstall_plugin(plugin_name):
    plugin_dir = Path.home() / ".minakishield" / "plugins"
    plugin_path = plugin_dir / f"{plugin_name}.py"
    if plugin_path.exists():
        plugin_path.unlink()
        click.echo(f"✅ Uninstalled plugin: {plugin_name}")
    else:
        click.echo(f"🛑 Plugin '{plugin_name}' not found.")
