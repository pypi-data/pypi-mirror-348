import typer
from .about_author import about_author
from .crud import create_alias, delete_alias, show_aliases, edit_aliases, source_shell_profile, flush_aliases
from .sync import sync_aliasify
from .assets.alerts import *

app = typer.Typer(help="Aliases Keeper - Manage and synchronize your aliases")

@app.command()
def about():
    """Display a welcome message"""
    info('Welcome to Aliases Keeper!')
    success(about_author())

@app.command()
def create(alias_name: str = typer.Argument(...), alias_value: str = typer.Argument(...), group: str = typer.Option("Other", "--group", "-g")):
    """Create a new alias"""
    create_alias(alias_name, alias_value, group)
    source_shell_profile()

@app.command()
def delete(alias_name: str = typer.Argument(...)):
    """Delete an alias by name"""
    delete_alias(alias_name)
    source_shell_profile()

@app.command()
def edit(alias_name: str = typer.Argument(...), alias_value: str = typer.Argument(...), group: str = typer.Option("Other", "--group", "-g")):
    """Edit an alias by name"""
    edit_aliases(alias_name, alias_value, group)
    source_shell_profile()

@app.command()
def show():
    """Show the Current Aliases"""
    show_aliases()
    source_shell_profile()

@app.command()
def flush():
    """Flush all the aliases."""
    if typer.confirm('All the saved aliases will be flushed. Do you want to continue?'):
        flush_aliases()
        source_shell_profile()

@app.command()
def sync(direction: str = typer.Option('local-to-remote', "--direction", "-d", help="Sync direction: 'local-to-remote' or 'remote-to-local'", show_choices=True, case_sensitive=False)):
    """Sync aliases between local and remote Dotfiles repository."""
    sync_aliasify(direction)

if __name__ == "__main__":
    app()
