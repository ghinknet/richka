# Richka - Python Async Download Engine

![Project Version](https://img.shields.io/pypi/v/richka) ![Python Version](https://img.shields.io/pypi/pyversions/richka)

#### Richka (From Ukrainian: Рiчка) means river, stands for the download speed of Richka Engine

## Usage

`import richka` and run script in your code, for example:

```
import richka

import asyncio
import time
import threading

# Create task controller
controller = richka.Controller()

def download():
    global controller

    # Create download task
    time_used, file_size = asyncio.run(richka.download("https://mirrors.tuna.tsinghua.edu.cn/videolan-ftp/vlc-iOS/3.6.4/VLC-iOS.ipa", "VLC-iOS.ipa", controller))

    # Result
    print("Time used:", time_used)
    print(f"Speed: {file_size / time_used / pow(1024, 2)}MiB/s")

def main():
    global controller

    # Progress monitor
    while controller.status:
        if controller.status == 1:
            print(f"Download Progress: {round(controller.progress, 2)}%         \r", end="")
        time.sleep(0.1)

if __name__ == "__main__":
    threading.Thread(target=download).start()
    main()

```
Then you'll get a file from Internet :D.