import click
from cneura_ai.commands import DockerManager

docker_manager = DockerManager()


@click.group()
@click.version_option("0.1.58")
def cli():
    """CNeura CLI - Autonomous service Orchestration"""
    pass


@cli.command()
def version():
    """Show the current version."""
    click.echo("🧠 CNeura AI version 0.1.58")


@cli.command()
def run():
    """Run all services."""
    click.echo("🚀 Running services ...")
    config_path = "./configs/run.json"
    try:
        docker_manager.load_from_config(config_path)
        click.echo("✅ Microservices started successfully.")
    except Exception as e:
        click.echo(f"❌ Failed to start microservices: {e}")


@cli.command()
@click.argument("service_name")
def status(service_name):
    """Check status of a service."""
    click.echo(f"🔍 Checking status of service: {service_name}...")
    containers = docker_manager.list_running_containers()
    related = [c for c in containers if service_name in c['name']]
    if related:
        for c in related:
            click.echo(f"📦 {c['name']} | Status: {c['status']} | Ports: {c['ports']}")
    else:
        click.echo(f"⚠️ No running containers found for service '{service_name}'.")


@cli.command()
@click.argument("service_name")
def delete(service_name):
    """Stop and delete a service."""
    click.confirm(f"⚠️ Are you sure you want to delete service '{service_name}'?", abort=True)
    docker_manager.delete_container(service_name)


@cli.command()
def list_services():
    """List all currently running services."""
    containers = docker_manager.list_running_containers()
    if not containers:
        click.echo("🚫 No running containers found.")
        return

    click.echo("📚 Running Services:")
    for c in containers:
        click.echo(f" - {c['name']} | Status: {c['status']} | Ports: {c['ports']}")


@cli.command()
def stop_all():
    """Stop all running containers."""
    click.confirm("⚠️ This will stop ALL running containers. Continue?", abort=True)
    docker_manager.stop_all()


@cli.command()
def init():
    """Run initial required containers."""
    config_path = "./configs/init.json"
    try:
        docker_manager.load_from_config(config_path)
        click.echo("✅ Initial required containers started successfully.")
    except Exception as e:
        click.echo(f"❌ Failed to start initial containers: {e}")


def main():
    cli()


if __name__ == "__main__":
    main()
