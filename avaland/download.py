# -*- coding: utf-8 -*-

import math
import os
try:
    import pathlib
except ImportError:
    import pathlib2
import sys
import time

import requests
from requests import HTTPError, ConnectionError

from avaland.exceptions import SourceNetworkError


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%.2f %s" % (s, size_name[i])


class Download:
    def __init__(self, title, artist, url, path=None):
        self.url = url
        self.file_name = title + " - " + artist + ".mp3"
        self.path = os.path.abspath(os.path.expanduser(path)) if path else os.path.join(os.getcwd(), artist)

    def get(self):
        if os.path.isfile(os.path.join(self.path, self.file_name)):
            self.path = os.path.join(self.path, self.file_name)
            return
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(self.path, self.file_name), "wb") as f:
            start = time.time()
            try:
                req = requests.get(self.url, stream=True)
            except ConnectionError:
                raise SourceNetworkError("Cannot download this music.")
            except HTTPError:
                raise SourceNetworkError("Cannot download this music. (HTTPError)")
            total_length = req.headers.get("content-length")
            if total_length is None:
                f.write(req.content)
            else:
                dl = 0
                total_length = int(total_length)
                print("Downloading: %s" % self.file_name.split(".")[0])
                for data in req.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    percent = " " + str(done) if done < 10 else done
                    sys.stdout.write("\r%s%%|%s%s| (%s / %s) %s/s    " % (
                        percent, "█" * int(done // 3), " " * (int((33 - done // 3))), convert_size(dl),
                        convert_size(total_length), convert_size(int(dl // (time.time() - start))).replace(" ", "")))
                    sys.stdout.flush()
        print()
        self.path = os.path.join(self.path, self.file_name)

    def __repr__(self):
        return "{cls}(url={url}, path={path})".format(cls=Download.__name__, url=self.url, path=self.path)
