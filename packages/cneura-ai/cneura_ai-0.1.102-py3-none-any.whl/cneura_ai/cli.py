import click
from cneura_ai.commands import DockerManager
from cneura_ai.config import CLIConfig

docker_manager = DockerManager()


@click.group()
@click.version_option(CLIConfig.VERSION)
@click.option("--config", type=click.Path(exists=True), help="Override config file path (JSON)")
def cli(config):
    """CNeura CLI - Autonomous service orchestration"""
    CLIConfig.ensure_paths()
    if config:
        try:
            CLIConfig.apply_override(config)
            click.echo(f"✅ Loaded custom config: {config}")
        except Exception as e:
            click.echo(f"❌ Failed to load config override: {e}")


@cli.command()
def version():
    """Show the current version."""
    click.echo("🧠 CNeura AI version 0.1.58")


@cli.command()
def run():
    """Run all services."""
    click.echo("🚀 Running services ...")
    # config_path = "./configs/run.json"
    try:
        docker_manager.load_from_config(CLIConfig.run_config_override or CLIConfig.DEFAULT_RUN_CONFIG)
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
    # config_path = "./configs/init.json"
    try:
        docker_manager.load_from_config(CLIConfig.init_config_override or CLIConfig.DEFAULT_INIT_CONFIG)
        click.echo("✅ Initial required containers started successfully.")
    except Exception as e:
        click.echo(f"❌ Failed to start initial containers: {e}")




def main():
    cli()


if __name__ == "__main__":
    main()
