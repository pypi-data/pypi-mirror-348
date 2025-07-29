from __future__ import annotations
from logging import *
import typing as t

KISESI_DEFAULT_FORMAT_STRING = (
    "[%(asctime)s] %(levelname)s @ %(filename)s:%(lineno)d %(funcName)s :: %(message)s"
)
NOT_SET = NOTSET

class LoggerLike(Logger):
    def __getattr__(self, name: str): 
        return getattr(self, name)

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    REVERSE = "\033[7m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class ColoredFormatter(Formatter):
    LEVEL_COLORS = {
        DEBUG: Color.BRIGHT_CYAN,
        INFO: Color.BRIGHT_GREEN,
        WARNING: Color.BRIGHT_YELLOW,
        ERROR: Color.BRIGHT_RED,
        CRITICAL: f"{Color.BG_RED}{Color.BRIGHT_WHITE}",
    }
    LEVEL_NAMES = {
        WARNING: "WARN",
    }

    def format(self, record: LogRecord):
        level_color = self.LEVEL_COLORS.get(record.levelno, "")
        level_name = self.LEVEL_NAMES.get(record.levelno, record.levelname)
        record.levelname = f"{level_color}[{level_name}]{Color.RESET}"
        return super().format(record)


def _get_default_kisesi_handler(fmt: t.Any, datefmt: t.Any):
    handler = StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt, datefmt=datefmt))
    return handler


def _monkeypatch_logger(logger: t.Any) -> LoggerLike | None:
    if not logger:
        return None

    # somewhere down the line in recursion, it returns a `logging.RootLogger`,
    # we handle that case here by not patching a `logging.RootLogger`
    if not isinstance(logger, Logger): # type: ignore
        return logger

    if getattr(logger, "__KISESI__", False):
        return logger # type: ignore

    logger = t.cast(Logger, t.Any)
    logger.set_level = logger.setLevel
    logger.is_enabled_for = logger.isEnabledFor
    logger.get_child = lambda *args, **kwargs: _monkeypatch_logger( # type: ignore
        logger.getChild(*args, **kwargs)
    )
    logger.get_children = lambda *args, **kwargs: _monkeypatch_logger( # type: ignore
        logger.getChildren(*args, **kwargs)
    )
    logger.add_filter = logger.addFilter
    logger.remove_filter = logger.removeFilter
    logger.find_caller = logger.findCaller
    logger.make_record = logger.makeRecord
    logger.has_handlers = logger.hasHandlers
    logger.add_handler = logger.addHandler

    # We abuse getattribute dunder method to lazily 
    # monkeypatch parent logger only when necessary
    logger.__class__ = type(
        logger.__class__.__name__,
        (logger.__class__,),
        dict(
            __getattribute__=lambda self, name: ( # type: ignore
                object.__getattribute__(self, name) # type: ignore
                if name != "parent"
                else _monkeypatch_logger(object.__getattribute__(self, "parent")) # type: ignore
            )
        ),
    )

    logger.__KISESI__ = True # type: ignore

    return logger


def get_logger(name: str | None = None):
    return _monkeypatch_logger(getLogger(name))


def basic_config(*, incdate: bool = False, use12h: bool = True, **kwargs: t.Any):
    if not kwargs.get("format"):
        kwargs["format"] = KISESI_DEFAULT_FORMAT_STRING

    if not kwargs.get("datefmt"):
        if use12h:
            kwargs["datefmt"] = "%I:%M:%S %p"
        else:
            kwargs["datefmt"] = "%T"

        if incdate:
            kwargs["datefmt"] = "%D " + kwargs["datefmt"]

    if not kwargs.get("handlers"):
        kwargs["handlers"] = [
            _get_default_kisesi_handler(kwargs.get("format"), kwargs.get("datefmt"))
        ]

    return basicConfig(**kwargs)
