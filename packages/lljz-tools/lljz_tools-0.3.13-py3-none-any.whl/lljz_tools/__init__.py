# coding=utf-8

__version__ = '0.3.13'

from .log_manager import LogManager
from .models import Model, ReadOnlyModel
from .random_tools import RandomTools
from .console_table import ConsoleTable
from .color import Color


logger = LogManager('lljz-tools', console_level='DEBUG').get_logger()


__all__ = [
    'Model',
    'ReadOnlyModel',
    'LogManager',
    'logger', 
    'RandomTools',
    'ConsoleTable',
    'Color',
]
if __name__ == '__main__':
    pass
