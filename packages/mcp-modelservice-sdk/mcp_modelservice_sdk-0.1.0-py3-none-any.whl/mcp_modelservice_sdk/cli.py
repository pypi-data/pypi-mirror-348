import typer
from typing_extensions import Annotated # For Typer type hints

from mcp_modelservice_sdk.service import run_server

app = typer.Typer(
    help="MCP Modelservice CLI: Run and manage the modelservice.",
    add_completion=False, # Can be enabled if desired
)

@app.command()
def run(
    host: Annotated[str, typer.Option(help="Host to bind the server to.")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port to bind the server to.")] = 8080,
    log_level: Annotated[str, typer.Option(help="Logging level (e.g., info, debug, warning).")] = "info",
):
    """
    Start the Modelservice FastAPI server.
    """
    run_server(host=host, port=port, log_level=log_level)

if __name__ == "__main__":
    app() 