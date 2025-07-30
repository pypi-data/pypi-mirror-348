# MIT License

# Copyright (c) 2022-present Rahman Yusuf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hashlib
import logging
import os
import re
import threading
import time

from enum import Enum
from .chinfo import get_chapter_info as get_chinfo
from ..language import Language
from ..downloader import FileDownloader
from ..utils import get_cover_art_url
from .. import __repository__, __url_repository__
from ..progress_bar import progress_bar_manager as pbm

log = logging.getLogger(__name__)


def get_chapter_info(manga, chapter, path):
    pbm.logger.info(f"Creating chapter info for '{chapter.get_name()}'")

    vol_cover = get_volume_cover(
        manga=manga, volume=chapter.volume, path=None, replace=False, download=False
    )

    if vol_cover is None:
        pbm.logger.debug(
            f"Failed to get volume cover for '{chapter.get_name()}' chapter info. "
            "Falling back to manga cover..."
        )
        vol_cover = manga.cover

    image = get_chinfo(manga, vol_cover, chapter)
    image.save(path)

    return path


def get_volume_cover(manga, volume, path, replace, download=True):
    # "Circular Imports" problem
    from ..iterator import CoverArtIterator

    if download:
        pbm.logger.info(f'Getting volume cover for "Volume {volume}"')

    # Find volume
    def find_volume_cover(cover):
        if volume is None:
            # There is higher change
            # that "null" volume is "volume 0"
            return cover.volume == 0

        return volume == cover.volume

    cover_art_iter_kwargs = [
        # Fix default volume covers behaviour
        # See https://github.com/mansuf/mangadex-downloader/issues/105
        {"language_override": None},  # --volume-cover-language or --language
        {
            "language_override": manga.original_language.value,
        },  # volume cover from manga original language
        {
            "language_override": "all",
        },  # Volume cover from any languages that exists
    ]

    cover = None
    for kwargs in cover_art_iter_kwargs:
        kwargs["manga_id"] = manga.id
        iterator = CoverArtIterator(**kwargs)
        f = filter(find_volume_cover, iterator)

        try:
            cover = next(f)
        except StopIteration:
            lang = Language(iterator.language)
            log.debug(f"Failed to find volume cover in {lang.name} language")
            continue
        else:
            break

    if download and cover is None:
        pbm.logger.warning(
            f"Failed to find volume cover for volume {volume}. "
            "Falling back to manga cover..."
        )
        cover = manga.cover

    url = get_cover_art_url(manga.id, cover, "original")

    if download:
        fd = FileDownloader(url, path, replace=replace)
        fd.download()
        fd.cleanup()

    return cover


class NumberWithLeadingZeros:
    """A helper class for parsing numbers with leading zeros

    total argument can be iterable or number
    """

    def __init__(self, total):
        try:
            iter_total = iter(total)
        except TypeError:
            if not isinstance(total, int):
                raise ValueError("total must be iterable or int") from None
            total_num = total
        else:
            total_num = 0
            for _ in iter_total:
                total_num += 1

        self._total = total_num
        self._num = 0

    def reset(self):
        self._num = 0

    def increase(self, num=1):
        self._num += num

    def decrease(self, num=1):
        self._num -= num

    def get_without_zeros(self):
        """This will return number without leading zeros"""
        return str(self._num)

    def get(self):
        num_str = str(self._num)
        return num_str.zfill(len(str(self._total)))


class Sha256RegexError(Exception):
    """Raised when regex_sha256 cannot grab sha256 from server_file object"""

    pass


def get_md_file_hash(server_file):
    """Get sha256 hash from MangaDex image filename"""
    # Yes this is very cool regex
    regex_sha256 = r"-(?P<hash>.{1,})\."

    # Get sha256 hash from server file
    match = re.search(regex_sha256, server_file)
    if match is None:
        raise Sha256RegexError(
            f"Failed to grab sha256 hash from server_file = {server_file}. "
            f"Please report it to {__url_repository__}/{__repository__}/issues"
        )

    server_hash = match.group("hash")

    return server_hash


def verify_sha256(file_hash, path=None, data=None):
    """Verify file hash with SHA256

    Parameters
    -----------
    file_hash: :class:`str`
        SHA256 hash in ASCII hex format
    path: Optional[Union[:class:`str`, :class:`bytes`, :class:`pathlib.Path`]]
        File want to be verified
    data: Optional[:class:`bytes`]
        Image data wants to be verified
    """
    local_sha256 = hashlib.sha256()

    if path:
        # File is not exist
        if not os.path.exists(path):
            return None

        # Begin verifying
        size = 8192
        with open(path, "rb") as reader:
            while True:
                data = reader.read(size)
                if not data:
                    break

                local_sha256.update(data)
    elif data:
        local_sha256.update(data)

    return local_sha256.hexdigest() == file_hash


def create_file_hash_sha256(path):
    s = hashlib.sha256()

    if not os.path.exists(path):
        return None

    size = 8192
    with open(path, "rb") as reader:
        while True:
            data = reader.read(size)
            if not data:
                break

            s.update(data)

    return s.hexdigest()


# Compliance with Tachiyomi local JSON format
class MangaStatus(Enum):
    Ongoing = "1"
    Completed = "2"
    Hiatus = "6"
    Cancelled = "5"


class QueueWorkerReadMarker(threading.Thread):
    """A queue-based worker run in another thread for ChapterReadMarker

    This class will mark chapter as read for every 20 chapters
    and will be done asynchronously (in another thread)
    """

    def __init__(self, manga_id) -> None:
        threading.Thread.__init__(self)

        # "Circular Imports" problem
        from ..network import Net, base_url

        self.net = Net
        self.base_url = base_url

        self._shutdown = threading.Event()
        self._chapters = []
        self._max_size = 20

        self.manga_id = manga_id

        cls_name = self.__class__.__name__
        # Thread to check if mainthread is alive or not
        # if not, then thread queue must be shutted down too
        self._thread_wait_mainthread = threading.Thread(
            target=self._wait_mainthread,
            name=f"{cls_name}-wait-mainthread, {cls_name}_id={self.ident}",
        )

        self.name = f"{cls_name}, {cls_name}_id={self.ident}"

    def start(self):
        super().start()
        self._thread_wait_mainthread.start()

    def _wait_mainthread(self):
        """Wait for mainthread to exit and then shutdown :class:`QueueWorker` thread"""
        main_thread = threading.main_thread()

        while True:
            main_thread.join(timeout=1)
            if not self.is_alive():
                # QueueWorker already shutted down
                # Possibly because of QueueWorker.shutdown() is called
                return
            elif not main_thread.is_alive():
                # Main thread already shutted down
                # and QueueWorker still alive, terminate it
                self._shutdown.set()
                return

    def submit(self, chapter_id):
        """Submit a chapter id that will marked as read"""
        self._chapters.append(chapter_id)

    def shutdown(self, blocking=False):
        if not self.is_alive():
            return

        self._shutdown.set()

        if blocking:
            self.join()

    def run(self):
        while True:
            if self._shutdown.is_set() and not self._chapters:
                # Shutdown signal is received
                # make sure there is nothing left in queue
                return

            # We're trying to get 20 chapter_ids
            # while shutdown signal has not been received yet
            # If somehow shutdown signal received, it should send whatever last in queue
            if len(self._chapters) < self._max_size and not self._shutdown.is_set():
                time.sleep(0.5)
                continue

            chapter_ids = self._chapters[: self._max_size - 1]
            del self._chapters[: self._max_size - 1]

            data = {"chapterIdsRead": chapter_ids}

            url = f"{self.base_url}/manga/{self.manga_id}/read"
            r = self.net.mangadex.post(url, json=data)

            if not r.ok:
                log.error(
                    "An error occurred when marking chapters as read. "
                    "Re-adding failed chapters to queue"
                )
                # obviously we don't wanna flood the screen with bunch of chapter ids
                log.debug(f"Failed chapters to marked as read: {chapter_ids}")

                self._chapters.extend(chapter_ids)
                continue
