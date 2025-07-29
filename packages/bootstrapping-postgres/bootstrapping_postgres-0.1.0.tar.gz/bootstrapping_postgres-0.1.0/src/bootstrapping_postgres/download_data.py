import itertools
import pathlib
import ssl
from asyncio import TaskGroup

import httpx
from rich.progress import Progress, SpinnerColumn, TaskID

SSL_CONTEXT = ssl.create_default_context()
YEARS =['2022', '2023', '2024', '2025']
MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

async def download_file(client: httpx.AsyncClient,
                         url: str,
                         output_folder: pathlib.Path,
                         task_id: TaskID,
                         progress: Progress) -> None:
    """Download a file asynchronously and update the progress bar."""
    output_file = output_folder / url.split("/")[-1]
    if output_file.exists():
        progress.update(task_id, advance=1, description=f"Already downloaded {output_file.name}")
        return
    resp = await client.get(url)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        progress.update(task_id, advance=1, description=f"Failed to download {url}: {exc}")
        return

    with open(output_file, "wb") as f:
        f.write(resp.content)
    progress.update(task_id, advance=1, description=f"Downloaded {output_file.name}")

async def download_trips_data(output_folder: pathlib.Path) -> None:
    """Download trips data for the specified years and months."""
    with Progress(SpinnerColumn(finished_text="✓"), "{task.description}") as progress:
        async with httpx.AsyncClient(base_url='https://d37ci6vzurychx.cloudfront.net/trip-data', verify=SSL_CONTEXT,
                                     timeout=30) as client:
            async with TaskGroup() as tg:
                for year, month in itertools.product(YEARS, MONTHS):
                    url = f"yellow_tripdata_{year}-{month}.parquet"
                    year_folder = output_folder / "trips" / year
                    year_folder.mkdir(parents=True, exist_ok=True)
                    progress_task = progress.add_task(f"Downloading {url}", total=1)
                    tg.create_task(download_file(client, url, year_folder, progress_task, progress))