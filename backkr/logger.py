from aiohttp.abc import AbstractAccessLogger
import datetime
from enum import Enum

import rong


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4


class Logger:
    '''
    Logger class to log messages based on the log level.
    This class is used to log messages to the console.
    '''

    def __init__(self, level: LogLevel) -> None:
        self.level = level

    def debug(self, message: str) -> None:
        '''
        This method is used to log debug messages.
        '''
        if self.level.value <= LogLevel.DEBUG.value:
            _time_log = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            rong.Text(
                text=f'[{_time_log}] [DEBUG] {message}',
                fg=rong.ForegroundColor.GREEN,
            ).print()

    def info(self, message: str) -> None:
        '''
        This method is used to log info messages.
        '''
        if self.level.value <= LogLevel.INFO.value:
            _time_log = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            rong.Text(
                text=f'[{_time_log}] [INFO] {message}',
                fg=rong.ForegroundColor.BLUE,
            ).print()

    def warn(self, message: str) -> None:
        '''
        This method is used to log warning messages.
        '''
        if self.level.value <= LogLevel.WARN.value:
            _time_log = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            rong.Text(
                text=f'[{_time_log}] [WARNING] {message}',
                fg=rong.ForegroundColor.YELLOW,
            ).print()

    def error(self, message: str) -> None:
        '''
        This method is used to log error messages.
        '''
        if self.level.value <= LogLevel.ERROR.value:
            _time_log = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            rong.Text(
                text=f'[{_time_log}] [ERROR] {message}',
                fg=rong.ForegroundColor.RED,
            ).print()

    def critical(self, message: str) -> None:
        '''
        This method is used to log critical messages.
        '''
        if self.level.value <= LogLevel.CRITICAL.value:
            _time_log = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            rong.Text(
                text=f'[{_time_log}] [CRITICAL] {message}',
                fg=rong.ForegroundColor.VIOLET
            ).print()

    def __str__(self) -> str:
        return "<Logger object>"

    def __repr__(self) -> str:
        return "<Logger object>"


def set_color(text: str, fg: rong.ForegroundColor, end: bool = False) -> str:
    '''
    This function is used to color the text based on the foreground color.
    '''
    if end:
        return f'{fg.value}{text}{rong.Style.CLEAR.value}'
    return f'{fg.value}{text}'


def status_color(status: int) -> rong.ForegroundColor:
    '''
    This function is used to return the color based on the status code.
    '''
    if status >= 100 and status < 200:
        return rong.ForegroundColor.BLUE
    elif status >= 200 and status < 300:
        return rong.ForegroundColor.GREEN
    elif status >= 300 and status < 400:
        return rong.ForegroundColor.YELLOW
    elif status >= 400 and status < 500:
        return rong.ForegroundColor.RED
    elif status >= 500:
        return rong.ForegroundColor.RED
    else:
        return rong.ForegroundColor.WHITE


class RouteLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        _time_log = set_color(
            "[" + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "]",
            rong.ForegroundColor.GREEN
        )
        method = set_color("[" + request.method + "]",
                           rong.ForegroundColor.BLUE)
        time_str = set_color(
            f'{time * 1000:.3f}ms',
            rong.ForegroundColor.GREEN
        )
        status = set_color(
            str(response.status),
            status_color(response.status),
            end=True
        )
        path = set_color(
            "\"" + request.path + "\"",
            status_color(response.status)
        )

        # Set the total width for the log entry
        total_width = 80

        # Create the base log entry without dots
        base_log_entry = f'{_time_log} {method} {path} '

        # Calculate the number of dots needed
        dots_count = total_width - \
            len(base_log_entry) - len(status) - len(time_str) + 20
        # dots = '.' * dots_count
        dots = set_color('.' * dots_count, rong.ForegroundColor.LIGHTWHITE)

        # Create the final log entry
        log_entry = f'{base_log_entry}{dots} {time_str} - {status}'

        # Print the log entry with the desired color
        print(log_entry)
