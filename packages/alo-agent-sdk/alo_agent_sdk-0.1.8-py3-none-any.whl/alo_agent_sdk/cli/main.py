import typer
import shutil
import pathlib
import importlib.resources
import importlib.util # Added import
import os # Added import

app = typer.Typer() # Simplified initialization

@app.command()
def hello():
    """A minimal command with no arguments."""
    typer.echo("Hello from ALO SDK CLI!")

# Keep the create_app command for now, but it won't be the default if hello is called
@app.command() # Removed explicit name="create-app", will default to function name "create_app"
def create_app(template_name: str, output_dir_str: str): # Restored output_dir_str argument
    """
    Creates a new application project from a specified template.

    Args:
        template_name: Name of the project template to use (e.g., 'mana').
        output_dir_str: Directory where the project will be created.
    
    Example: alo-sdk create-app mana ./my_mana_project
    """
    typer.echo(f"Creating new application from template '{template_name}' in '{output_dir_str}'...")
    output_dir = pathlib.Path(output_dir_str)

    # DEBUG: Remove output directory if it exists to allow repeated tests (can be removed later)
    if output_dir.exists():
        typer.echo(f"Warning: Output directory '{output_dir}' already exists. Removing for test.")
        try:
            shutil.rmtree(output_dir)
        except Exception as e:
            typer.secho(f"Could not remove existing directory {output_dir}: {e}", fg=typer.colors.RED)
            # For debug, we might proceed or exit. Let's try to proceed.

    try:
        # Try to find the templates directory within the installed package
        # This relies on `project_templates` being packaged with `alo_agent_sdk`
        # and accessible via `importlib.resources`.
        # The structure assumed is:
        # alo_agent_sdk (package)
        #  └── project_templates
        #      └── mana
        #          └── ...
        
        # Construct the path to the specific template directory
        # This is for checking existence, actual path for copying is derived later using importlib.resources.files
        template_check_path = f"alo_agent_sdk.project_templates.{template_name}"
        
        # Check if the template module/package exists
        try:
            # Ensure importlib.util is available
            if importlib.util.find_spec(template_check_path) is None:
                 typer.secho(f"Error: Template package spec '{template_check_path}' not found. This might mean the template sub-package doesn't exist or isn't structured as a module.", fg=typer.colors.RED)
                 # For this to work, alo_agent_sdk/project_templates/mana needs an __init__.py if mana is a package
                 # Or, we just check for directory existence using importlib.resources.files later.
                 # Let's rely on the directory check for now.
                 # raise typer.Exit(code=1) # Commenting out this check for now, will rely on is_dir() below
        except ModuleNotFoundError: # This specific exception might not be hit if find_spec returns None
            typer.secho(f"Error: Template '{template_name}' module structure not found. Ensure 'alo_agent_sdk.project_templates.{template_name}' is discoverable.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # Use importlib.resources to access the template files
        # The `files()` function refers to the contents of a package.
        # If project_templates is a sub-package of alo_agent_sdk:
        source_template_dir_traversable = importlib.resources.files("alo_agent_sdk").joinpath("project_templates", template_name)

        if not source_template_dir_traversable.is_dir():
            typer.secho(f"Error: Template source '{template_name}' is not a directory or not found at expected location: {source_template_dir_traversable}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # shutil.copytree needs string paths or Path-like objects that are actual file system paths.
        # `importlib.resources.as_file` provides a context manager that yields a real file system path.
        with importlib.resources.as_file(source_template_dir_traversable) as source_path_concrete:
            if output_dir.exists() and list(output_dir.iterdir()):
                typer.secho(f"Error: Output directory '{output_dir}' already exists and is not empty.", fg=typer.colors.RED)
                raise typer.Exit(code=1)
            
            output_dir.mkdir(parents=True, exist_ok=True) # Ensure parent dirs exist, allow if output_dir itself was just created

            shutil.copytree(source_path_concrete, output_dir, dirs_exist_ok=True) # dirs_exist_ok for the target dir itself

        typer.secho(f"Successfully created project '{output_dir.name}' from template '{template_name}'.", fg=typer.colors.GREEN)
        typer.echo("\nNext steps:")
        typer.echo(f"  1. Navigate to the project: cd {output_dir}")
        if template_name == "mana":
            typer.echo("  2. Review the README.md inside the project for setup and usage instructions.")
            typer.echo("  3. Modify requirements if needed, especially for 'alo-agent-sdk' if using a local/dev version:")
            typer.echo("     - For local SDK development, edit 'requirements.sdk.txt' in 'agent_registry' and 'time_agent'")
            typer.echo("       to point to your local 'alo-agent-sdk' path (e.g., '../path/to/alo_agent_sdk') or a local wheel.")
            typer.echo("  4. Run locally using Docker: docker-compose up --build")
            typer.echo("  5. To deploy, configure and use the 'deploy_all.sh' script.")

    except FileNotFoundError:
        typer.secho(f"Error: Template '{template_name}' not found. Path resolution failed.", fg=typer.colors.RED)
        typer.echo("Ensure the 'project_templates' directory is correctly packaged with the SDK.")
        raise typer.Exit(code=1)
    except FileExistsError:
        # This should be caught by the earlier check, but as a safeguard.
        typer.secho(f"Error: Output directory '{output_dir}' already exists and is not empty.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
