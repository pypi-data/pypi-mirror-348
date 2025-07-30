import click
import os
from shield.core import (
    load_services,
    load_enabled_services,
    save_enabled_services,
    restart_shield_service
)

@click.group(help="Manage and run detection services.")
def services():
    pass

@services.command(name="list")
def list_services():
    """List all available services and their status (enabled/disabled)."""
    services = load_services()
    enabled_services = load_enabled_services()

    if not services:
        click.echo("⚠️ No detection services available.")
        return

    click.echo("🧩 Detection Services:")
    for name, _ in services:
        status = "🟢 Enabled" if name in enabled_services else "🔴 Disabled"
        click.echo(f"  ✅ {name} - {status}")

@services.command(name="enable")
@click.argument("service_name")
def enable_service(service_name):
    """Enable a specific detection service."""
    enabled_services = load_enabled_services()
    if service_name not in enabled_services:
        enabled_services.add(service_name)
        save_enabled_services(enabled_services)
        click.echo(f"✅ Enabled: {service_name}")
        restart_shield_service()
    else:
        click.echo(f"⚠️ {service_name} is already enabled.")

@services.command(name="disable")
@click.argument("service_name")
def disable_service(service_name):
    """Disable a specific detection service."""
    enabled_services = load_enabled_services()
    if service_name in enabled_services:
        enabled_services.remove(service_name)
        save_enabled_services(enabled_services)
        click.echo(f"❌ Disabled: {service_name}")
        restart_shield_service()
    else:
        click.echo(f"⚠️ {service_name} is not currently enabled.")
