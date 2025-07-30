import io
import keyword
import logging
import os
import re
import sys
import tokenize
from functools import wraps
from logging import Formatter as BaseFormatter
from os import PathLike
from pathlib import Path
from typing import TextIO, Callable, Optional, Literal, TypedDict

import better_exceptions
from colorlog import ColoredFormatter as CF  # noqa
from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

from .decorators import singleton


ColorString = Literal[
    'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white',
    'bold_red', 'bold_green', 'bold_yellow', 'bold_blue', 'bold_purple', 'bold_cyan', 'bold_white',
    'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_purple', 'light_cyan', 'light_white',
    ]
LevelNum = Literal[0, 5, 10, 20, 25, 30, 40]
LevelString = Literal['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'FATAL', 'CRITICAL', 'TRACE', 'SUCCESS']
Level = LevelNum | LevelString
ColorStringWithLevel = ColorString | Literal['level']

class LevelColorDict(TypedDict, total=False):
    TRACE: ColorString
    DEBUG: ColorString
    INFO: ColorString
    SUCCESS: ColorString
    WARNING: ColorString
    ERROR: ColorString
    CRITICAL: ColorString
    
class SecondaryLogColorDict(TypedDict, total=False):
    levelname: ColorStringWithLevel
    message: ColorStringWithLevel
    asctime: ColorStringWithLevel
    name: ColorStringWithLevel
    module: ColorStringWithLevel
    funcName: ColorStringWithLevel
    lineno: ColorStringWithLevel

default_level_colors: LevelColorDict = {
    "TRACE": "cyan",
    "DEBUG": "blue",
    "SUCCESS": "light_green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

default_secondary_log_colors: SecondaryLogColorDict = {
    "levelname": "level",
    "message": "level",
    "asctime": 'green',
    "name": 'purple',
    "module": 'cyan',
    "funcName": 'cyan',
    "lineno": 'cyan',
}


class ExceptionFormat:

    """
    将异常信息格式化
    """

    @staticmethod
    def _tokenize(source):
        # Worth reading: https://www.asmeurer.com/brown-water-python/
        source = source.encode("utf-8")
        source = io.BytesIO(source)

        try:
            yield from tokenize.tokenize(source.readline)
        except tokenize.TokenError:
            return

    @classmethod
    def _formate_code_line(cls, line: str):
        row = ''

        tokens = list(cls._tokenize(line))[1:]

        def add_row(index, val):
            if index == 0:
                return val
            else:
                sep = ' ' * (tokens[index].start[1] - tokens[index - 1].end[1])
                return sep + val

        for i, token in enumerate(tokens):
            if token.type == tokenize.COMMENT:
                row += add_row(i, '\033[37;3m' + token.string + '\033[0m')
            elif token.type == tokenize.NAME:
                # 如果是keyword，则变为紫色
                if token.string in keyword.kwlist:
                    row += add_row(i, '\033[35;1m' + token.string + '\033[0m')
                else:
                    row += add_row(i, token.string)
            elif token.type == tokenize.NUMBER:
                row += add_row(i, '\033[32m' + token.string + '\033[0m')
            elif token.type == tokenize.STRING:
                row += add_row(i, '\033[36m' + token.string + '\033[0m')
            else:
                row += add_row(i, token.string)
        return row + '\n'

    @classmethod
    def _formate_exception_line(cls, line):
        is_code = False

        for inner_line in line.split('\n'):
            if is_code:
                yield cls._formate_code_line(inner_line)
                is_code = False
            elif inner_line.startswith('  File "'):
                obj = re.match(
                    r'^\s+File "(?P<filename>[^"]+)", line (?P<lineno>\d+), in (?P<name>[^"]+)$',
                    inner_line
                )
                if obj:
                    yield (f'\n  \033[31mFile "{obj.group("filename")}", line\033[0m '
                           f'\033[33m{obj.group("lineno")}\033[0m\033[31m, in \033[0m'
                           f'\033[35m{obj.group("name")}\033[0m\n')
                    is_code = True
                else:
                    yield inner_line + '\n'
            else:
                yield '\033[36m' + inner_line + '\033[0m\n'

    @classmethod
    def format_exception(cls, exc_info):
        formatter = better_exceptions.ExceptionFormatter(colored=False)
        for line in formatter.format_exception(*exc_info):
            if line == 'Traceback (most recent call last):\n':
                yield '\033[33;1mTraceback (most recent call last):\n\033[0m'
            elif line == '\nThe above exception was the direct cause of the following exception:\n\n':
                yield '\n\033[31mThe above exception was the direct cause of the following exception:\n\n\033[0m'
            elif line == '\nDuring handling of the above exception, another exception occurred:\n\n':
                yield '\n\033[31mDuring handling of the above exception, another exception occurred:\n\n\033[0m'
            elif not line.startswith(' '):
                error, *message = line.split(':', maxsplit=1)
                line = f'\033[31;1m{error}\033[0m'
                if message:
                    line += f':{"".join(message)}'
                yield line
            else:
                yield from cls._formate_exception_line(line)


class ColoredFormatter(CF):

    """
    支持颜色配置的日志格式，支持的颜色参考ColorString中的配置
    """

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = None,
            log_colors: Optional[LevelColorDict] = None,
            reset: bool = True,
            secondary_log_colors: SecondaryLogColorDict | None = None,
            level_colors: LevelColorDict | None = None,
            style: Literal['{', '%', '$'] = '{',
    ) -> None:
        level_colors = level_colors or default_level_colors
        secondary_log_colors = secondary_log_colors or default_secondary_log_colors
        secondary_log_colors_mapper = {
            k: ({lv: v for lv in logging._nameToLevel} if v != 'level' else level_colors)  
            for k, v in secondary_log_colors.items()
        }
        if not fmt:
            fmt = default_fmt

        for k in secondary_log_colors_mapper.keys():
            if style == '{':
                fmt = re.sub(rf'({{{k}.*?}})', rf'{{{k}_log_color}}\1{{reset}}', fmt)
            elif style == '%':
                fmt = re.sub(rf'(%\({k}.*?\)s)', rf'%({k}_log_color)s\1%(reset)s', fmt)
            elif style == '$':
                fmt = re.sub(rf'(\${{{k}.*?}})', rf'${{{k}_log_color}}\1${{reset}}', fmt)
            else:
                raise ValueError('style only support \'{\' or \'%\' or \'$\'')
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            log_colors=log_colors,  # type: ignore
            reset=reset,
            secondary_log_colors=secondary_log_colors_mapper,  # type: ignore
        )

    def format(self, record):
        if record.exc_info:
            if not getattr(record, '_is_better_exception', False):
                record.exc_text = ''.join(ExceptionFormat.format_exception(record.exc_info))
                record._is_better_exception = True
        return super().format(record)


class Formatter(BaseFormatter):

    def format(self, record):
        """
        对于异常堆栈信息，美化展示格式

        :param record:
        :return:
        """
        if record.exc_info:
            # 此处需要判断是否已经美化过了，如果已经美化，则不需要重复美化
            # 通过_is_better_exception属性来进行判断
            if not getattr(record, '_is_better_exception', False):
                record.exc_text = ''.join(ExceptionFormat.format_exception(record.exc_info))
                record._is_better_exception = True
        return re.sub(r'\033\[.+?m', '', super().format(record))


ColoredFormatter.default_msec_format = '%s.%03d'
Formatter.default_msec_format = '%s.%03d'
BaseFormatter.default_msec_format = '%s.%03d'

TRACE = 5
SUCCESS = 25
logging.addLevelName(TRACE, "TRACE")
logging.addLevelName(SUCCESS, "SUCCESS")
default_fmt = '{asctime} | {levelname:<8} | {name} | {module}:{funcName}:{lineno} - {message}'
default_console_format = ColoredFormatter(default_fmt)
default_file_format = Formatter(default_fmt, style='{')
default_format = BaseFormatter(default_fmt, style='{')


class ManagerLogger(logging.Logger):

    def catch_exception(self, func: Callable):
        """捕获异常，自动打印错误日志"""

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.exception(f'{func.__name__}执行错误：[{e.__class__.__name__}]{e}', stacklevel=2)

        return inner

    def record_exception(self, func: Callable):
        """仅记录异常"""

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.exception(f'{func.__name__}执行错误：[{e.__class__.__name__}]{e}', stacklevel=2)
                raise e

        return inner

    def _add_console_handler(self, stream=None, level: Optional[Level] = None, formatter: str | Formatter | None = None,
                             filters: Callable | list[Callable] | None = None):
        if stream is None:
            stream = sys.stdout
        handler = logging.StreamHandler(stream)
        if not formatter:
            formatter = default_console_format  # type: ignore
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        handler.setLevel(level)  # type: ignore
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def _add_file_handler(self, path: str | PathLike, level: Optional[Level] = None, formatter: str | Formatter | None = None,
                          filters: Callable | list[Callable] | None = None):
        handler = ConcurrentTimedRotatingFileHandler(
            path,
            when="midnight",
            backupCount=10,
            encoding="utf-8",
            delay=True,
            maxBytes=10 * 1024 * 1024,
        )
        handler.setLevel(level)  # type: ignore
        if not formatter:
            formatter = default_file_format
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def remove(self, handler=None):
        if handler:
            return self.removeHandler(handler)
        else:
            self.handlers.clear()

    def add(self, sink: TextIO | str | PathLike, *, level: Level = "DEBUG", formatter=None, filters=None):
        kwargs = dict(level=level, filters=filters, formatter=formatter)
        if sink is sys.stdout or sink is sys.stderr:
            return self._add_console_handler(sink, **kwargs)
        else:
            return self._add_file_handler(sink, **kwargs)

    def success(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            SUCCESS, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )

    def trace(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            TRACE, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )

def reset_logger(
        __logger: logging.Logger,
        /, *,
        fmt=default_fmt,
        file_path='/pythonlogs/out.log',
        error_file_path='/pythonlogs/error.log',
        colorize=True,
        no_console=False,
        console_level: Level = 'DEBUG',
        file_level: Level = 'INFO',
        error_file_level: Level = 'ERROR'
) -> ManagerLogger:
    """
    重新设置日志格式

    :param __logger: 日志对象
    :param fmt: 日志消息格式
    :param file_path: 日志文件路径，为空时不记录，默认/pythonlogs/out.log
    :param error_file_path: ERROR级别的日志文件路径，为空时不记录，默认/pythonlogs/error.log
    :param colorize: 是否启用控制台颜色，默认为True
    :param no_console: 是否启用控制台日志，默认为False
    :param console_level: 控制台中的日志最低级别，默认DEBUG
    :param file_level: 日志文件中的日志最低级别，默认INFO
    :param error_file_level: 错误文件中的日志最低级别，默认ERROR
    :return:
    """
    if not isinstance(__logger, ManagerLogger):
        handlers, filters, name, level = __logger.handlers, __logger.filters, __logger.name, __logger.level
        __logger = ManagerLogger(name, level)
        __logger.handlers = handlers
        __logger.filters = filters

    __logger.remove()
    style = LogManager.guess_fmt_style(fmt)
    ConsoleFormatter = ColoredFormatter if colorize else BaseFormatter
    file_format = Formatter(fmt, style=style)
    console_format = ConsoleFormatter(fmt, style=style)
    if not no_console:
        __logger.add(sys.stdout, level=console_level, formatter=console_format)
    if file_path:
        __logger.add(file_path, level=file_level, formatter=file_format)
    if error_file_path:
        __logger.add(error_file_path, level=error_file_level, formatter=file_format)

    return __logger

def _get_loger(name=None):
    __logger = getLogger_raw(name)
    __logger_new = ManagerLogger(__logger.name, __logger.level)
    __logger_new.handlers = __logger.handlers
    __logger_new.filters = __logger.filters
    return __logger_new

getLogger_raw = logging.getLogger


logging.getRawLogger, logging.getLogger = logging.getLogger, _get_loger



class _NOT_SET_CLS: pass  # noqa


_NOT_SET = _NOT_SET_CLS()


class LogManager:

    def __init__(
            self, __name: str, *,
            console_level: Level = "DEBUG",
            file_path: str | _NOT_SET_CLS | None = _NOT_SET,
            file_level: Level = "DEBUG",
            file_name: str = 'out.log',
            error_level: Level  = "ERROR",
            error_file_name: str = 'error.log',
            fmt: str = default_fmt,
            colorize: bool = True,
    ) -> None:
        logging.root.setLevel(logging.NOTSET)
        self._file_path = self._init_log_file_path(file_path)
        if self._file_path and not self._file_path.exists():
            os.mkdir(self._file_path)
        self.console_level = console_level
        self.file_level = file_level
        self.error_level = error_level
        self._logger: ManagerLogger = _get_loger(__name)
        self.fmt = fmt
        self.colorize = colorize
        self.file_name = file_name
        self.error_file_name = error_file_name
        

    @staticmethod
    def _init_log_file_path(file_path: str | PathLike | _NOT_SET_CLS | None = _NOT_SET) -> Path | None:
        if file_path is None:
            return None
        if file_path is not _NOT_SET:
            return Path(file_path)  # type: ignore
        if "PYTHONPATH" in os.environ and os.path.exists(os.environ['PYTHONPATH']):
            return Path(os.environ['PYTHONPATH']) / 'logs'
        return Path('/pythonlogs')

    @staticmethod
    def guess_fmt_style(fmt: str) -> Literal['{', '%', '$']:
        for i in fmt:
            if i == '{':
                return '{'
            if i == '%':
                return '%'
            if i == '$':
                return '$'
        raise ValueError(f'无法识别的日志格式：{fmt!r}')

    def get_logger(self) -> ManagerLogger:
        """
        获取logger对象
        """
        file_path = error_file_path = ""
        if self._file_path is not None and self.file_level:
            file_path = self._file_path / self.file_name
        if self._file_path is not None and self.error_level:
            error_file_path = self._file_path / self.error_file_name

        return reset_logger(
            self._logger,
            fmt=self.fmt,
            file_path=file_path,
            error_file_path=error_file_path,
            colorize=self.colorize,
            no_console=False,
            console_level=self.console_level,
            file_level=self.file_level,
            error_file_level=self.error_level,
        )


    @property
    def logger(self):
        return self._logger

if __name__ == '__main__':
    logger = LogManager(__name__, console_level='TRACE', file_path='./../logs').get_logger()


    def func1(a, b):
        return a / b


    @logger.catch_exception
    def func2():
        return func1(1, 0)


    func2()
