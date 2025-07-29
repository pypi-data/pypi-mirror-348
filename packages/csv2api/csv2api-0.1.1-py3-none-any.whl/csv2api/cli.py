import typer
from csv2api.app import run_api

app = typer.Typer()

@app.command()
def run(file: str ):
    """Start the API server for a given CSV file."""
    run_api(file)


