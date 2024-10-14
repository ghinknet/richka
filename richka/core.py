import time
import asyncio

import richka

import aiohttp

async def __download_range(session: aiohttp.ClientSession, url: str, start: int, end: int, destination: str) -> None:
    richka.logger.info(f'Downloading part {start}-{end} of {url} to {destination}.')

    headers = {**richka.HEADERS, **{'range': f'bytes={start}-{end}'}}

    async with session.get(url, headers=headers) as response:
        content = await response.read()
        with open(destination, 'r+b') as f:
            f.seek(start)
            f.write(content)

    richka.logger.info(f'Downloaded part {start}-{end} of {destination}.')

async def __download_single(session: aiohttp.ClientSession, url: str, destination: str) -> None:
    richka.logger.info(f'Downloading {url} to {destination}.')

    async with session.get(url, headers=richka.HEADERS) as response:
        content = await response.read()
        with open(destination, 'r+b') as f:
            f.write(content)

    richka.logger.info(f'Downloaded {url} to {destination}.')

async def download(url: str, destination: str) -> float:
    async with aiohttp.ClientSession() as session:
        # Get file size
        async with session.head(url) as response:
            file_size = int(response.headers.get('Content-Length', 0))

        if not file_size or file_size / pow(1024, 2) <= 10:
            if not file_size:
                richka.logger.info(f'Failed to get file size, directly downloading {url}.')
            else:
                richka.logger.info(f"Downloading {url} ({file_size}) to {destination} with signle mode.")

            # Create an empty file
            with open(destination, 'wb') as f:
                f.truncate(file_size)

            # Start task
            start_time = time.time()
            await __download_single(session, url, destination)
            end_time = time.time()
            return end_time - start_time

        richka.logger.info(f'Downloading {url} ({file_size}) to {destination} with slicing mode.')

        # Calc slice size
        part_size = file_size // richka.COROUTINE_LIMIT

        # Create an empty file
        with open(destination, 'wb') as f:
            f.truncate(file_size)

        # Create coroutine tasks
        tasks = []
        for i in range(richka.COROUTINE_LIMIT):
            start = i * part_size
            end = (start + part_size - 1) if i < richka.COROUTINE_LIMIT - 1 else (file_size - 1)
            task = __download_range(session, url, start, end, destination)
            tasks.append(task)

        # Start all task
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
        return end_time - start_time