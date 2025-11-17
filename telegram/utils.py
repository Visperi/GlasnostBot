"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import logging
from datetime import datetime, UTC
from typing import (
    Union,
    List,
    Type,
    TypeVar,
    Any,
    Dict,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from .media import File


T = TypeVar("T")


class MediaCacheItem:

    def __init__(self, created: datetime, file: 'File'):
        """
        A cache item for ``MediaCache``. Encapsulates ``telegram.File`` objects with their creation time to make their
        handling easier.

        :param created: Datetime when the item was created.
        :param file: A ``telegram.File`` stored in the cache.
        """
        self.created = created
        self.file = file

    @property
    def has_expired(self) -> bool:
        """
        :return: True if the file was created at least an hour ago and is expired. False otherwise.
        """
        diff = datetime.now(UTC) - self.created
        return diff.total_seconds() >= 3600


class MediaCache:

    def __init__(self):
        """
        A minimalistic cache for storing Telegram files requested from their API so a new ``getfile`` request is not
        needed every time.
        """
        self._cache: Dict[str, MediaCacheItem] = {}

    def __getitem__(self, file_unique_id: str):
        return self._cache[file_unique_id]

    def __delitem__(self, file_unique_id: str):
        del self._cache[file_unique_id]

    def add(self, file: 'File'):
        """
        Add a ``telegram.File`` object to the cache.

        :param file: The file to add to cache.
        """
        self._cache[file.file_unique_id] = MediaCacheItem(datetime.now(UTC), file)

    def get(self, file_unique_id: str, default: Any = None) -> Union['File', Any]:
        """
        Get a ``telegram.File`` object from the cache if found. If not found or the file has expired, return the default value
        instead. Files will expire after an hour.

        :param file_unique_id: The file unique ID.
        :param default: Value to return if the file is not found from cache.
        :return: The ``telegram.File`` object or the default value.
        """
        try:
            cache_item = self[file_unique_id]
        except KeyError:
            return default

        if cache_item.has_expired:
            del self[file_unique_id]
            return default
        else:
            return cache_item.file


class _CustomFormatter(logging.Formatter):
    """
    A default log formatter with colours.
    """

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    output_format = "[{asctime}] [{levelname:<8}] {name}: {message}"

    LEVEL_COLOURS = [
        (logging.DEBUG, grey),
        (logging.INFO, grey),
        (logging.WARNING, yellow),
        (logging.ERROR, red),
        (logging.CRITICAL, bold_red)
    ]

    FORMATTERS = {}
    for level, colour in LEVEL_COLOURS:
        FORMATTERS[level] = logging.Formatter(fmt=colour+output_format+reset, datefmt="%Y-%m-%d %H:%M:%S", style="{")

    def format(self, record) -> str:
        formatter = self.FORMATTERS.get(record.levelno, self.FORMATTERS[logging.DEBUG])

        if record.exc_info:
            formatted = formatter.formatException(record.exc_info)
            record.exc_text = self.red + formatted + self.reset

        output = formatter.format(record)
        record.exc_text = None
        return output


def configure_logging(
        level: Union[int, str] = logging.INFO,
        formatter: logging.Formatter = None,
        handler: logging.Handler = None,
        use_colours: bool = True) -> None:
    """
    Configure logging for the logging system.
    :param level: The smallest logging level to log.
    :param formatter: Formatter for the log messages. If omitted, a default one is set up with or without colours
    depending on parameter use_colours.
    :param handler: Handler for the logger. If omitted, StreamHandler is used with default parameters.
    :param use_colours: Choose if colour should be used for the logging. Has no effect if formatter is explicitly
    given to this function.
    """

    if not handler:
        handler = logging.StreamHandler()

    if not formatter and use_colours:
        formatter = _CustomFormatter()
    else:
        formatter = logging.Formatter(fmt="[{asctime}] [{levelname:<8}] {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S",
                                      style="{")

    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)


def flatten_handlers(cls: Type[T]) -> Type[T]:
    """
    Decorator method for flattening class attribute handler methods to list of tuples (attr_name, handler_func).

    :param cls: The class instance
    :return: The class instance with flattened handlers.
    """
    prefix = "_handle_"
    handlers = [(key[len(prefix):], value) for key, value in cls.__dict__.items() if key.startswith(prefix)]

    cls._HANDLERS = handlers
    return cls


# TODO: Replace these two methods below with class structure that works out of the box
# TODO: (Or just wait better support for identifiers as TypedDict attributes)
def replace_dictionary_keys(original: Union[dict, list]):
    new_dict = {}
    key_dict = {"from": "from_"}

    if isinstance(original, list):
        dict_value_list = list()

        for inner_dict in original:
            dict_value_list.append(replace_dictionary_keys(inner_dict))

        return dict_value_list

    else:
        for key in original.keys():
            value = original[key]
            new_key = key_dict.get(key, key)

            if isinstance(value, dict) or isinstance(value, list):
                new_dict[new_key] = replace_dictionary_keys(value)
            else:
                new_dict[new_key] = value

        return new_dict


def replace_builtin_keywords(json: List[dict]) -> List[dict]:
    return [replace_dictionary_keys(d) for d in json]
