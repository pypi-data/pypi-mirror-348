import requests
import time
import os
import json
import importlib
import pkgutil
from pathlib import Path
import shield.services
import yaml

def load_config():
    config_path = Path.home() / ".minakishield" / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

#def load_services():
#    services = []
#    for loader, name, ispkg in pkgutil.iter_modules(shield.services.__path__):
#        module = importlib.import_module(f'shield.services.{name}')
#        if hasattr(module, 'detect'):
#            services.append((name, module.detect))
#            print(f"✅ Loaded: {name}")
#    return services

from pathlib import Path
import importlib
import pkgutil
import json

SERVICE_DIR = Path(__file__).parent / "services"
SERVICES_CONFIG = Path.home() / ".minakishield" / "services_enabled.json"
SYSTEMD_SERVICE_NAME = "minakishield.service"

#def load_enabled_services():
#    if SERVICES_CONFIG.exists():
#        with open(SERVICES_CONFIG, "r") as f:
#            try:
#                return set(json.load(f))
#            except json.JSONDecodeError:
#                return set()
#    return set()

def load_enabled_services():
    """Load enabled services from config or auto-enable all available ones if missing."""
    if SERVICES_CONFIG.exists():
        try:
            with open(SERVICES_CONFIG, "r") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            pass  # Fall through to regenerate with defaults

    # 🧠 Dynamically detect all valid services
    from shield.services import __path__ as services_path
    default_services = set()

    for loader, name, ispkg in pkgutil.iter_modules(services_path):
        try:
            module = importlib.import_module(f'shield.services.{name}')
            if hasattr(module, 'detect'):
                default_services.add(name)
        except Exception as e:
            print(f"⚠️ Failed to load service {name}: {e}")

    save_enabled_services(default_services)
    return default_services

def save_enabled_services(enabled_services):
    with open(SERVICES_CONFIG, "w") as f:
        json.dump(list(enabled_services), f)

def restart_shield_service():
    click.echo("🔄 Restarting MinakiShield service...")
    os.system(f"systemctl --user restart {SYSTEMD_SERVICE_NAME}")
    click.echo("✅ MinakiShield service restarted.")

def load_services():
    """Load only services that are enabled in the JSON config."""
    services = []
    enabled = load_enabled_services()

    for loader, name, ispkg in pkgutil.iter_modules([str(SERVICE_DIR)]):
        if name in enabled:
            try:
                module = importlib.import_module(f'shield.services.{name}')
                detect = getattr(module, 'detect', None)
                if detect:
                    services.append((name, detect))
                    print(f"✅ Loaded: {name}")
                else:
                    print(f"⚠️ Skipped {name}: no detect() function.")
            except Exception as e:
                print(f"❌ Failed to load {name}: {e}")
    return services

import importlib
import pkgutil
from pathlib import Path
import click

PLUGIN_DIR = Path.home() / ".minakishield" / "plugins"

def load_plugins():
    plugins = []

    # Check if the plugin directory exists
    if not PLUGIN_DIR.exists():
        PLUGIN_DIR.mkdir(parents=True, exist_ok=True)

    # Dynamically load plugins from the plugin directory
    for plugin_path in PLUGIN_DIR.glob("*.py"):
        plugin_name = plugin_path.stem  # Get the file name without extension
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the plugin has a 'cli' command
            if hasattr(module, 'cli') and isinstance(module.cli, click.Command):
                plugins.append((plugin_name, module.cli))
            else:
                print(f"⚠️ Skipping invalid plugin: {plugin_name} (no 'cli' command found)")
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_name}: {e}")

    return plugins

def monitor_logs(logfiles, services, log_to_file=False, json_output=False, webhook_url=None):
    config = load_config()
    webhook_url = webhook_url or config.get("webhook_url")
    file_pointers = {}
    log_file_path = Path.home() / ".minakishield" / "shield.log"

    if webhook_url:
        print(f"📡 Webhook URL active: {webhook_url}")

    if log_to_file:
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"📝 Logging alerts to {log_file_path}")

    def log_alert(rule_name, line):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = line.strip()
        short_message = extract_message(msg)

        json_payload = {
            "timestamp": timestamp,
            "rule": rule_name.upper(),
            "message": short_message,
            "raw": msg
        }

        slack_payload = {
            "text": f"🚨 *{rule_name.upper()}* detected at `{timestamp}`:\n```{short_message}```"
        }

        # Output to console
        if json_output:
            print(json.dumps(json_payload))
        else:
            print(f"[ALERT] {rule_name.upper()}: {msg}")

        # Write to file
        if log_to_file:
            with open(log_file_path, 'a') as log_file:
                if json_output:
                    log_file.write(json.dumps(json_payload) + '\n')
                else:
                    log_file.write(f"[{timestamp}] [ALERT] {rule_name.upper()}: {msg}\n")

        # Send to Slack/Webhook
        if webhook_url:
            try:
                print(f"📤 Sending to webhook: {webhook_url}")
                print(f"📦 Payload:\n{json.dumps(slack_payload, indent=2)}")
                response = requests.post(webhook_url, json=slack_payload, timeout=5)
                response.raise_for_status()
            except Exception as e:
                print(f"⚠️ Webhook failed: {e}")

    def extract_message(line):
        parts = line.split(':', 2)
        return parts[2].strip() if len(parts) > 2 else line.strip()

    for path in logfiles:
        try:
            fp = open(path, 'r')
            fp.seek(0, os.SEEK_END)
            file_pointers[path] = fp
            print(f"👁️ Now watching: {path}")
        except Exception as e:
            print(f"❌ Cannot open {path}: {e}")

    try:
        while True:
            for path, fp in file_pointers.items():
                where = fp.tell()
                line = fp.readline()
                if not line:
                    time.sleep(0.1)
                    fp.seek(where)
                else:
                    for name, detect in services:
                        if detect(line):
                            log_alert(name, line)
    except KeyboardInterrupt:
        print("\n🛑 Stopped monitoring.")
    finally:
        for fp in file_pointers.values():
            fp.close()
