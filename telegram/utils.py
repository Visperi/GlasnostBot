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
from typing import (
    Union,
    List,
    Type,
    TypeVar
)


T = TypeVar("T")


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
