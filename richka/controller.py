import asyncio

class Controller:
    def __init__(self):
        self.__paused = False
        self.__total_size = 0
        self.__downloaded_size = 0
        self.__downloaded_size_slice = {}
        self.__lock = asyncio.Lock()  # For async safe

    @property
    def total_size(self) -> int:
        """
        Get the total size of the file.
        :return: Integer Size of the file.
        """
        return self.__total_size

    @total_size.setter
    def total_size(self, size: int) -> None:
        """
        Set the total size of the file.
        :param size: Integer Size of the file.
        :return: None
        """
        if not self.__total_size:
            self.__total_size = size

    async def update_progress(self, downloaded_chunk_size: int, chunk_id: str = None) -> None:
        """
        Update the progress of the download. Do not operate this!
        :param downloaded_chunk_size: Integer Downloaded Size of the file.
        :param chunk_id: String Chunk ID of the part.
        :return: None
        """
        async with self.__lock:
            if chunk_id is None and self.__downloaded_size_slice == {}:
                self.__downloaded_size = downloaded_chunk_size
            else:
                self.__downloaded_size_slice[chunk_id] = downloaded_chunk_size
                self.__downloaded_size = sum(self.__downloaded_size_slice.values())

    @property
    def paused(self) -> bool:
        """
        Get the paused state of the downloader.
        :return: Boolean State of the downloader.
        """
        return self.__paused

    def pause(self) -> None:
        """
        Pause the downloader.
        :return: None
        """
        self.__paused = True

    def unpause(self) -> None:
        """
        Unpause the downloader.
        :return: None
        """
        self.__paused = False

    @property
    def status(self) -> int:
        """
        Get the status of the downloader.
        :return: Integer Status of the downloader. -1: Haven't Started -2: Paused 0: Done 1: Downloading
        """
        if self.__downloaded_size == 0:
            return -1 # Haven't started
        elif self.__paused:
            return -2 # Paused
        elif self.__downloaded_size / self.__total_size == 1:
            return 0 # Done
        else:
            return 1 # Downloading

    @property
    def progress(self) -> float:
        """
        Get the progress of the downloader.
        :return: Float Progress of the downloader.
        """
        if not self.__total_size:
            return -1
        return self.__downloaded_size / self.__total_size * 100
