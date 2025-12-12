import typer
from typing_extensions import Annotated

from llm_orchestration_hw6.__version__ import __version__ # Corrected import

app = typer.Typer(help="LLM Agent Orchestration CLI for evaluating prompt engineering techniques.")

def version_callback(value: bool):
    if value:
        print(f"LLM Agent Orchestration HW6 Version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
):
    """
    Manage the LLM Agent Orchestration Framework.
    """
    pass

@app.command()
def hello(name: str = "World"):
    """
    A simple command to test the CLI is working.
    """
    print(f"Hello {name}!")

if __name__ == "__main__":
    app()