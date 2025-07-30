"""
Command-line interface for GitHub Account Manager.
"""

import os
import sys
import click
from pathlib import Path
from ghswitch.account import AccountManager
from ghswitch.platforms import get_platform_handler

@click.group()
def cli():
    """GitHub Account Manager - Manage multiple GitHub accounts on a single device."""
    pass

@cli.command()
@click.option("--name", required=True, help="A unique name for this account")
@click.option("--username", required=True, help="GitHub username")
@click.option("--email", required=True, help="Email associated with the GitHub account")
@click.option("--ssh-key", help="Path to SSH key (optional)")
@click.option("--token", help="GitHub personal access token (optional)")
@click.option("--generate-key", is_flag=True, help="Generate a new SSH key if none is provided")
def add(name, username, email, ssh_key, token, generate_key):
    """Add a new GitHub account."""
    manager = AccountManager()
    success, message = manager.add_account(name, username, email, ssh_key, token, generate_key)
    
    if success:
        click.secho(message, fg="green")
        if generate_key and not ssh_key:
            platform = get_platform_handler()
            ssh_key_path = platform.get_ssh_dir() / f"id_rsa_{name}.pub"
            if ssh_key_path.exists():
                click.echo(f"\nA new SSH key has been generated at: {ssh_key_path}")
                click.echo("Add this key to your GitHub account:")
                with open(ssh_key_path, 'r') as f:
                    click.echo(f.read().strip())
    else:
        click.secho(message, fg="red")
        sys.exit(1)

@cli.command()
def list():
    """List all configured GitHub accounts."""
    manager = AccountManager()
    accounts = manager.list_accounts()
    
    if not accounts:
        click.echo("No accounts configured. Add one with 'ghswitch add'.")
        return
    
    click.echo("\nConfigured GitHub accounts:")
    click.echo("==========================")
    
    for account in accounts:
        name = account["name"]
        if account["is_primary"]:
            name += " (primary)"
        
        click.echo(f"\n{name}")
        click.echo(f"  Username: {account['username']}")
        click.echo(f"  Email: {account['email']}")
        if account["ssh_key"]:
            click.echo(f"  SSH Key: {account['ssh_key']}")

@cli.command(name="set-primary")
@click.argument("name")
def set_primary(name):
    """Set the primary GitHub account."""
    manager = AccountManager()
    success, message = manager.set_primary(name)
    
    if success:
        click.secho(message, fg="green")
    else:
        click.secho(message, fg="red")
        sys.exit(1)

@cli.command()
@click.argument("name")
@click.option("--global", "global_config", is_flag=True, help="Set as global Git config")
@click.option("--repo", help="Path to the repository (if not current directory)")
def use(name, global_config, repo):
    """Use a specific GitHub account."""
    manager = AccountManager()
    success, message = manager.use_account(name, global_config, repo)
    
    if success:
        click.secho(message, fg="green")
    else:
        click.secho(message, fg="red")
        sys.exit(1)

@cli.command()
@click.argument("name")
def remove(name):
    """Remove a GitHub account."""
    manager = AccountManager()
    success, message = manager.remove_account(name)
    
    if success:
        click.secho(message, fg="green")
    else:
        click.secho(message, fg="red")
        sys.exit(1)

@cli.command()
def current():
    """Show the current GitHub account being used."""
    manager = AccountManager()
    name, account = manager.get_current_account()
    
    if not account:
        click.echo("No account configured. Add one with 'ghswitch add'.")
        return
    
    click.echo(f"\nCurrent GitHub account: {name}")
    click.echo(f"  Username: {account['username']}")
    click.echo(f"  Email: {account['email']}")
    if account["ssh_key"]:
        click.echo(f"  SSH Key: {account['ssh_key']}")

if __name__ == "__main__":
    cli()
