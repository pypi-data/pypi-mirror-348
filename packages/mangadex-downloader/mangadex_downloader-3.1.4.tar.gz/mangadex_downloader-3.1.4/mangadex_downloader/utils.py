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

import os
import re
import time
import logging
import sys
import threading
import queue
import itertools
from pathlib import Path
from typing import List  # noqa: F401
from pathvalidate import sanitize_filename
from getpass import getpass
from concurrent.futures import Future
from .errors import InvalidURL

log = logging.getLogger(__name__)


def validate_url(url):
    """Validate mangadex url and return the uuid"""
    re_url = re.compile(
        r"([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})"
    )
    match = re_url.search(url)
    if match is None:
        raise InvalidURL('"%s" is not valid MangaDex URL' % url)
    return match.group(1)


def validate_legacy_url(url):
    """Validate old mangadex url and return the id"""
    re_url = re.compile(r"mangadex\.org\/(title|manga|chapter)\/(?P<id>[0-9]{1,})")
    match = re_url.search(url)
    if match is None:
        raise InvalidURL('"%s" is not valid MangaDex URL' % url)
    return match.group("id")


def validate_group_url(url):
    """Validate group mangadex url and return the id"""
    if url is None:
        return
    all_group = url.lower().strip() == "all"
    if not all_group:
        return validate_url(url)
    else:
        return "all"


def create_directory(name, path=None) -> Path:
    """Create directory with ability to sanitize name to prevent error"""
    base_path = Path(".")

    # User defined path
    if path:
        base_path /= path

    base_path /= sanitize_filename(name)
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path


# This is shortcut to extract data from localization dict structure
# in MangaDex JSON data
# For example:
# {
#     'attributes': {
#         'en': '...' # This is what we need
#     }
# }
def get_local_attr(data):
    if not data:
        return ""
    for key, val in data.items():
        return val


def input_handle(*args, **kwargs):
    """Same as input(),
    except when user hit EOFError the function automatically called sys.exit(0)"""
    try:
        return input(*args, **kwargs)
    except EOFError:
        sys.exit(0)


def getpass_handle(*args, **kwargs):
    """Same as getpass(),
    except when user hit EOFError the function automatically called sys.exit(0)"""
    try:
        return getpass(*args, **kwargs)
    except EOFError:
        sys.exit(0)


def comma_separated_text(array, use_bracket=True):
    text = ""

    # Opening square bracket
    if use_bracket:
        text += "["

    # Append first item
    try:
        text += array.pop(0)
    except IndexError:
        return ""

    # Add the rest of items
    for item in array:
        text += ", " + item

    # Closing square bracket
    if use_bracket:
        text += "]"

    return text


def delete_file(file):
    """Helper function to delete file, retry 5 times if error happens"""
    if not os.path.exists(file):
        return

    err = None
    for attempt in range(20):
        try:
            os.remove(file)
        except Exception as e:
            log.debug(
                'Failed to delete file "%s", reason: %s. Trying... (attempt: %s)'
                % (file, str(e), attempt)
            )
            err = e
            time.sleep(attempt * 0.5)  # Possible value 0.0 (0 * 0.5) lmao
            continue
        else:
            break

    # If 5 attempts is failed to delete file (ex: PermissionError, or etc.)
    # raise error
    if err is not None:
        raise err


queueworker_active_threads = []  # type: List[QueueWorker]


class QueueWorker(threading.Thread):
    """A queue-based worker run in another thread"""

    def __init__(self) -> None:
        threading.Thread.__init__(self)

        self._queue = queue.Queue()
        self._shutdown_signal = threading.Event()
        self.daemon = True

        # Thread to check if mainthread is alive or not
        # if not, then thread queue must be shutted down too
        self._thread_wait_mainthread = threading.Thread(
            target=self._wait_mainthread,
            name=f"QueueWorker-wait-mainthread, QueueWorker_id={self.ident}",
        )

        cls_name = self.__class__.__name__
        self.name = f"{cls_name}, {cls_name}_id={self.ident}"

    def start(self):
        super().start()
        self._thread_wait_mainthread.start()

        queueworker_active_threads.append(self)

    def _wait_mainthread(self):
        """Wait for mainthread to exit and then shutdown :class:`QueueWorker` thread"""
        main_thread = threading.main_thread()

        while True:
            main_thread.join(timeout=1)
            if not self.is_alive() or self._shutdown_signal.is_set():
                # QueueWorker already shutted down
                # Possibly because of QueueWorker.shutdown() is called
                return
            elif not main_thread.is_alive():
                # Main thread already shutted down
                # and QueueWorker still alive, terminate it
                self._queue.put(None)
                return

    def submit(self, job, blocking=True):
        """Submit a job and return the result

        If ``blocking`` is ``True``, the function will wait until job is finished.
        If ``blocking`` is ``False``, it will return :class:`concurrent.futures.Future`.
        The ``job`` parameter must be function without parameters or lambda wrapped.
        """
        fut = Future()
        data = [fut, job]
        self._queue.put(data)

        if not blocking:
            return fut

        err = fut.exception()
        if err:
            raise err

        return fut.result()

    def shutdown(self, blocking=False, blocking_timeout=None):
        """Shutdown the thread by passing ``None`` value to queue"""
        self._queue.put(None)
        self._shutdown_signal.set()

        if blocking:
            self.join(timeout=blocking_timeout)

    def run(self):
        while True:
            data = self._queue.get()
            if data is None:
                # Shutdown signal is received
                # begin shutting down
                return

            fut, job = data
            try:
                job()
            except Exception as err:
                log.error("We have problem in queue worker", exc_info=err)
                fut.set_exception(err)
            else:
                fut.set_result(None)


def convert_int_or_float(value):
    err_int = None
    err_float = None

    try:
        return int(value)
    except ValueError as e:
        err_int = e

    try:
        return float(value)
    except ValueError as e:
        err_float = e

    raise err_float from err_int


def check_blacklisted_tags_manga(manga):
    from .config import env

    found_tags = []
    for manga_tag, blacklisted_tag_id in itertools.product(
        manga.tags, env.tags_blacklist
    ):
        if manga_tag.id != blacklisted_tag_id:
            continue

        found_tags.append(manga_tag)

    if found_tags:
        return True, found_tags
    else:
        return False, found_tags


def get_cover_art_url(manga_id, cover, quality):
    if quality == "none" or cover is None:
        return None

    # "Circular Imports" problem
    from .network import uploads_url

    if quality == "original":
        additional_file_ext = ""
    elif quality == "512px":
        additional_file_ext = ".512.jpg"
    elif quality == "256px":
        additional_file_ext = ".256.jpg"

    return "{0}/covers/{1}/{2}{3}".format(
        uploads_url, manga_id, cover.file, additional_file_ext
    )


def _build_url_regex(type):
    # Legacy support
    if "legacy-manga" in type:
        regex = r"mangadex\.org\/(title|manga)\/(?P<id>[0-9]{1,})"
    elif "legacy-chapter" in type:
        regex = r"mangadex\.org\/chapter\/(?P<id>[0-9]{1,})"
    elif type == "manga":
        regex = (
            r"mangadex\.org\/(title|manga)\/"
            r"(?P<id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})"
        )
    elif type == "cover":
        regex = (
            r"(?P<id>.+(mangadex\.org|uploads\.mangadex\.org)\/covers\/"
            r"([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}"
            r"-[a-z0-9]{12})\/([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]"
            r"{4}-[a-z0-9]{12})(\.[a-zA-Z]{1,})(\..+|))"
        )
    else:
        regex = (
            r"mangadex\.org\/%s\/(?P<id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})"
            % type
        )
    return regex


valid_url_types = [
    "manga",
    "list",
    "chapter",
    "legacy-manga",
    "legacy-chapter",
    "cover",
]

_urL_regexs = {i: _build_url_regex(i) for i in valid_url_types}


def find_md_urls(text):
    for type, regex in _urL_regexs.items():
        # Match pattern regex
        result = re.search(regex, text)
        if result is None:
            continue

        id = result.group("id")
        return id, type


def get_key_value(text, sep="="):
    split = text.strip().split(sep, maxsplit=1)
    key = split[0].lower()
    value = "".join(split[1:])
    return key, value


def create_manga_info(path, manga, replace):
    from .config import config
    from .manga import MangaInfo

    log.debug(f"Writing file 'manga_info.{config.manga_info_format}'")

    manga_info = MangaInfo(path, manga, replace)
    manga_info.write()

    return manga


def convert_start_end_from_negative(start_num, end_num, data):
    """Convert start and end numbers from negative to positive

    Use cases:
    - "--start-chapter"
    - "--end-chapter"
    - "--start-page"
    - "--end-page"
    """

    if start_num is None or end_num is None:
        return start_num, end_num

    if start_num >= 0 and end_num >= 0:
        return start_num, end_num

    start_num = convert_int_or_float(start_num)
    end_num = convert_int_or_float(end_num)

    # Remove chapters from last index to beginning that is not numbers
    # to make sure we can use legacy range chapters and pages
    # We don't need to sorting the array, because that's been already done
    # in mangadex_downloader.chapter.IteratorChapter._fill_data()
    filtered_data = []
    for num in data:
        try:
            a = convert_int_or_float(num)
        except ValueError:
            continue
        else:
            filtered_data.append(a)

    return filtered_data[start_num], filtered_data[end_num]
