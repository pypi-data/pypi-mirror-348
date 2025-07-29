import os
import json
import click
from debugonce_packages.storage import StorageManager

@click.group()
def cli():
    """CLI for DebugOnce."""
    pass

@click.command()
@click.argument('session_file', type=click.Path(exists=True))

def replay(session_file):
    """Replay a captured session."""
    with open(session_file, 'r') as f:
        session_data = json.load(f)

    function_name = session_data.get("function")
    args = session_data.get("args", [])
    kwargs = session_data.get("kwargs", {})
    exception = session_data.get("exception")

    click.echo("Replaying function with input") # Added line
    click.echo(f"Replaying function: {function_name}")
    click.echo(f"Arguments: {args}")
    click.echo(f"Keyword Arguments: {kwargs}")


    if exception:
        click.echo(f"Exception occurred: {exception}")
    else:
        click.echo(f"Replaying function: {function_name} with args: {args} and kwargs: {kwargs}")

@click.command()
@click.argument('session_file', type=click.Path(exists=True))
def export(session_file):
    """Export a bug reproduction script."""
    with open(session_file, 'r') as f:
        session_data = json.load(f)

    function_name = session_data.get("function")
    args = session_data.get("args", [])
    kwargs = session_data.get("kwargs", {})
    exception = session_data.get("exception")

    script_content = f"""# Bug Reproduction Script
def {function_name}(*args, **kwargs):
    # Add your function logic here
    print("Function called with arguments:", args, "and keyword arguments:", kwargs)

def replay_function():
    input_args = {args}
    input_kwargs = {kwargs}
    try:
        {function_name}(*input_args, **input_kwargs)
    except Exception as e:
        print("Exception occurred during replay:", e)

if __name__ == "__main__":
    replay_function()
"""

    export_file = os.path.splitext(session_file)[0] + "_replay.py"
    with open(export_file, 'w') as f:
        f.write(script_content)
    click.echo(f"Exported bug reproduction script to {export_file}")

@click.command()
def list():
    """List all captured sessions."""
    session_dir = ".debugonce"
    if not os.path.exists(session_dir):
        click.echo("No captured sessions found.")
        return
    sessions = os.listdir(session_dir)
    if not sessions:
        click.echo("No captured sessions found.")
    else:
        click.echo("Captured sessions:")
        for session in sessions:
            click.echo(f"- {session}")

@click.command()
def clean():
    """Clean all captured sessions."""
    session_dir = ".debugonce"
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            os.remove(os.path.join(session_dir, file))
        click.echo("Cleared all captured sessions.")
    else:
        click.echo("No captured sessions to clean.")

cli.add_command(replay)
cli.add_command(export)
cli.add_command(list)
cli.add_command(clean)

def main():
    """Entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main()