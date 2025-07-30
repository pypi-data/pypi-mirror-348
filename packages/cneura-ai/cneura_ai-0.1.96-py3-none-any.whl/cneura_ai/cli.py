import click
from cneura_ai.commands import DockerManager  # Assuming your class is here

docker_manager = DockerManager()  # instantiate here


@click.group()
@click.version_option("0.1.58")
def cli():
    """CNeura CLI - Autonomous Agent Orchestration"""
    pass


@cli.command()
@click.argument("name", default="World")
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name} 👋")


@cli.command()
def version():
    """Show the current version."""
    click.echo("CNeura AI version 0.1.58")


@cli.command()
@click.argument("agent_name")
def create(agent_name):
    """Create a new autonomous agent."""
    click.echo(f"🛠️ Creating new agent: {agent_name}...")


@cli.command()
def run():
    """Run an existing agent."""
    click.echo(f"🚀 Running agent...")
    config_path = f"./configs/run.json"
    try:
        docker_manager.load_from_config(config_path)
        click.echo(f"Microservices for agent started successfully.")
    except Exception as e:
        click.echo(f"Failed to start microservices : {e}")


@cli.command()
@click.argument("agent_name")
def status(agent_name):
    """Check status of an agent."""
    click.echo(f"🔍 Checking status of agent: {agent_name}...")
    # Could add status check by querying docker_manager containers related to agent_name
    containers = docker_manager.list_running_containers()
    related = [c for c in containers if agent_name in c['name']]
    if related:
        for c in related:
            click.echo(f"Container: {c['name']} | Status: {c['status']} | Ports: {c['ports']}")
    else:
        click.echo(f"No running containers found for agent '{agent_name}'.")


@cli.command()
@click.argument("agent_name")
def delete(agent_name):
    """Delete an agent."""
    click.confirm(f"Are you sure you want to delete agent '{agent_name}'?", abort=True)
    click.echo(f"🗑️ Agent '{agent_name}' deleted.")
    # You could implement stopping and removing containers here related to the agent


@cli.command()
def list_agents():
    """List all available agents."""
    # Just dummy data for now
    agents = ["agent_alpha", "agent_beta", "agent_gamma"]
    click.echo("🧠 Registered Agents:")
    for agent in agents:
        click.echo(f" - {agent}")


@cli.command()
def init():
    """Run initial required containers."""
    # Assuming initial containers config file path
    config_path = "./configs/init.json"
    try:
        docker_manager.load_from_config(config_path)
        click.echo("Initial required containers started successfully.")
    except Exception as e:
        click.echo(f"Failed to start initial containers: {e}")


def main():
    cli()


if __name__ == "__main__":
    main()
