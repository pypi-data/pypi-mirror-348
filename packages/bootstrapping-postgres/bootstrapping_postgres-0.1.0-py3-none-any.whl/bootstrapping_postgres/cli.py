import asyncio
import pathlib
from typing import Annotated

import typer

from bootstrapping_postgres.download_data import download_trips_data

app = typer.Typer()

DEFAULT_DATA_PATH = pathlib.Path.cwd().joinpath("data")

@app.command(name="download")
def download_taxi_trips(
        output_folder: Annotated[pathlib.Path, typer.Option("-o", "--output-folder")]
        = DEFAULT_DATA_PATH) -> None:
    """ Download taxi trips data from the web and save it to the specified folder."""
    asyncio.run(download_trips_data(output_folder))


@app.command(name="test")
def test() -> None:
    """ Test the application. """
    print("Test command executed.")