"""Console script for batch_executor."""
import batch_executor

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for batch_executor."""
    console.print("Replace this message by putting your code into "
               "batch_executor.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
