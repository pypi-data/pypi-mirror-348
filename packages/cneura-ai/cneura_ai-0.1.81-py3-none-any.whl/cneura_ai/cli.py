import click

@click.group()
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

def main():
    cli()
