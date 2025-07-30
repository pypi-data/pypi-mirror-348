import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

import pandas as pd
import typer
import uvicorn

# Change from default command to explicit subcommands
app = typer.Typer(add_completion=False)


def start_backend(files_info, host="127.0.0.1", port=8000) -> None:
    """Start the backend server."""
    from anyeval.backend.app import create_app

    if isinstance(files_info, str):
        # Single file case
        df = pd.read_parquet(files_info)
        file_name = os.path.basename(files_info)
        files_list = [{"name": file_name, "path": files_info}]
    else:
        # Multiple files case
        df = pd.concat(
            [pd.read_parquet(file_info["path"]) for file_info in files_info],
            ignore_index=True,
        )
        files_list = files_info

    # Create and run the app with the loaded data and files info
    api_app = create_app(df, files_list)
    uvicorn.run(api_app, host=host, port=port)


@app.command()
def run(
    parquet_path: Path = typer.Argument(
        ..., help="Parquet file or directory containing parquet files", exists=True,
    ),
    listen: str = typer.Option(
        "127.0.0.1", help="IP address to listen on (default: 127.0.0.1)",
    ),
    port: int = typer.Option(8000, help="Port to listen on (default: 8000)"),
    open_browser: bool = typer.Option(True, help="Automatically open browser (default: True)"),
) -> None:
    """Run evaluation for a parquet file or directory."""
    # Process the input path
    files_info = []

    if parquet_path.is_dir():
        # If it's a directory, get all parquet files
        for file_path in parquet_path.glob("*.parquet"):
            file_name = file_path.name
            typer.echo(f"Found parquet file: {file_name}")
            files_info.append({"name": file_name, "path": str(file_path)})

        if not files_info:
            typer.echo(f"Error: No parquet files found in directory '{parquet_path}'.")
            sys.exit(1)

    elif parquet_path.is_file() and str(parquet_path).endswith(".parquet"):
        # Single file case
        typer.echo(f"Processing single parquet file: {parquet_path}")
        files_info = str(parquet_path)

    else:
        typer.echo(f"Error: '{parquet_path}' is not a valid parquet file or directory.")
        sys.exit(1)

    # Start the backend in a separate thread
    backend_thread = threading.Thread(
        target=start_backend, args=(files_info, listen, port), daemon=True,
    )
    backend_thread.start()

    # Give the server a moment to start
    time.sleep(1)

    # Open the browser if open_browser is True
    typer.echo(f"Server running at http://{listen}:{port}")
    if open_browser:
        typer.echo("Opening browser")
        webbrowser.open(f"http://{listen}:{port}")

    typer.echo("Press Ctrl+C to stop the server")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Shutting down services...")

    sys.exit(0)


# Add this function to serve as a default command
@app.callback()
def callback() -> None:
    """AnyEval - Universal Evaluation for Gen AI."""


if __name__ == "__main__":
    app()
