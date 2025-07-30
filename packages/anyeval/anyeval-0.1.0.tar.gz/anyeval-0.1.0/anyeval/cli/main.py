import os
import subprocess
import sys
import webbrowser
import time
from pathlib import Path
import pandas as pd
import typer
import uvicorn
import threading

app = typer.Typer()

def start_backend(parquet_file: str):
    """Start the backend server."""
    from anyeval.backend.app import create_app
    
    # Load the parquet file
    df = pd.read_parquet(parquet_file)
    
    # Create and run the app with the loaded data
    api_app = create_app(df)
    uvicorn.run(api_app, host="127.0.0.1", port=8000)

@app.command()
def run(parquet_file: str):
    """Open a parquet file and start the evaluation UI."""
    # Verify the parquet file exists
    if not os.path.exists(parquet_file):
        typer.echo(f"Error: Parquet file '{parquet_file}' does not exist.")
        sys.exit(1)
    
    # Start the backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, args=(parquet_file,), daemon=True)
    backend_thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    # Open the browser
    typer.echo(f"Opening browser to http://127.0.0.1:8000")
    webbrowser.open("http://127.0.0.1:8000")
    
    typer.echo("Press Ctrl+C to stop the server")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Shutting down services...")
    
    sys.exit(0)

@app.command()
def merge(
    parquet_files: list[str] = typer.Argument(..., help="List of parquet files or directory containing parquet files"),
    output_file: str = typer.Argument(..., help="Output parquet file path")
):
    """Merge multiple parquet files into one."""
    all_dfs = []
    
    # Process all input files
    for path in parquet_files:
        if os.path.isdir(path):
            # If it's a directory, get all parquet files
            for file in Path(path).glob("*.parquet"):
                typer.echo(f"Processing {file}")
                df = pd.read_parquet(file)
                all_dfs.append(df)
        else:
            # It's a single file
            typer.echo(f"Processing {path}")
            df = pd.read_parquet(path)
            all_dfs.append(df)
    
    if not all_dfs:
        typer.echo("No parquet files found.")
        sys.exit(1)
    
    # Merge all dataframes
    merged_df = pd.concat(all_dfs, ignore_index=True)
    
    # Save to output file
    merged_df.to_parquet(output_file)
    typer.echo(f"Merged data saved to {output_file}")

if __name__ == "__main__":
    app() 