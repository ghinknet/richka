import time
import asyncio

import aiohttp

import richka
from .controller import Controller

async def __download_range(session: aiohttp.ClientSession, url: str, start: int, end: int, destination: str, controller: Controller = None) -> None:
    richka.logger.info(f'Downloading part {start}-{end} of {url} to {destination}.')

    headers = {**richka.HEADERS, **{'range': f'bytes={start}-{end}'}}
    retry_times = richka.RETRY_TIMES

    while retry_times > 0:
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(sock_read=richka.TIMEOUT, sock_connect=richka.TIMEOUT)) as response:
                with open(destination, 'r+b') as f:
                    f.seek(start)
                    # Read stream
                    length = 0
                    async for chunk in response.content.iter_chunked(richka.CHUNK_SIZE):
                        while controller.paused:
                            await asyncio.sleep(1)
                        # noinspection PyTypeChecker
                        f.write(chunk)
                        # noinspection PyTypeChecker
                        length += len(chunk)
                        # Update tracker
                        if controller is not None:
                            await controller.update_progress(length, chunk_id=f"{start}-{end}")
            break
        except (aiohttp.ClientError, asyncio.TimeoutError):
            retry_times -= 1
            richka.logger.info(f'Download part {start}-{end} of {url} to {destination} failed for {richka.RETRY_TIMES - retry_times} times, retrying...')
            await asyncio.sleep(1)

    if retry_times > 0:
        richka.logger.info(f'Downloaded part {start}-{end} of {url} to {destination}.')
    else:
        raise TimeoutError(f'Download part {start}-{end} of {url} to {destination} timed out.')

async def __download_single(session: aiohttp.ClientSession, url: str, destination: str, controller: Controller = None) -> None:
    richka.logger.info(f'Downloading {url} to {destination}.')

    retry_times = richka.RETRY_TIMES\

    while retry_times > 0:
        try:
            async with session.get(url, headers=richka.HEADERS, timeout=aiohttp.ClientTimeout(sock_read=richka.TIMEOUT, sock_connect=richka.TIMEOUT)) as response:
                with open(destination, 'r+b') as f:
                    # Read stream
                    length = 0
                    async for chunk in response.content.iter_chunked(richka.CHUNK_SIZE):
                        while controller.paused:
                            await asyncio.sleep(1)
                        # noinspection PyTypeChecker
                        f.write(chunk)
                        # noinspection PyTypeChecker
                        length += len(chunk)
                        # Update tracker
                        if controller is not None:
                            await controller.update_progress(length)
            break
        except (aiohttp.ClientError, asyncio.TimeoutError):
            retry_times -= 1
            richka.logger.info(f'Download {url} to {destination} failed for {richka.RETRY_TIMES - retry_times} times, retrying...')
            await asyncio.sleep(1)

    if retry_times > 0:
        richka.logger.info(f'Downloaded {url} to {destination}.')
    else:
        raise TimeoutError(f'Download {url} to {destination} timed out.')

async def download(url: str, destination: str, controller: Controller = None) -> tuple[float, int]:
    """
    Download a single file.
    :param url: String Source URL.
    :param destination: Destination Path.
    :param controller: Download Controller.
    :return: [Float, Integer] [Time Used, File Size]
    """
    async with aiohttp.ClientSession() as session:
        # Get file size
        async with session.head(url) as response:
            file_size = int(response.headers.get('Content-Length', 0))

        if not file_size or file_size / pow(1024, 2) <= richka.SLICE_THRESHOLD:
            if not file_size:
                richka.logger.info(f'Failed to get file size, directly downloading {url}.')
            else:
                richka.logger.info(f"Downloading {url} ({file_size}) to {destination} with single mode.")
                if controller is not None:
                    controller.total_size = file_size

            # Create an empty file
            with open(destination, 'wb') as f:
                f.truncate(file_size)

            # Start task
            start_time = time.time()
            await __download_single(session, url, destination, controller)
            end_time = time.time()
            richka.logger.info(f"Downloaded {url} ({file_size}) to {destination} with single mode.")
            return end_time - start_time, file_size

        richka.logger.info(f'Downloading {url} ({file_size}) to {destination} with slicing mode.')
        if controller is not None:
           controller.total_size = file_size

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
            task = __download_range(session, url, start, end, destination, controller)
            tasks.append(task)

        # Start all task
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
        richka.logger.info(f'Downloaded {url} ({file_size}) to {destination} with slicing mode.')
        return end_time - start_time, file_size
