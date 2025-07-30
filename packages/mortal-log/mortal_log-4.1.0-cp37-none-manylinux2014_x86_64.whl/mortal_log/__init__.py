#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 18:05
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .log_main import MortalLogMain


class MortalLog(MortalLogMain):
    """
    MortalLog 类继承自 MortalLogMain，用于处理日志记录功能。
    该类提供了多种日志级别的方法，并允许配置日志的输出方式。
    """

    def __init__(self, title=None, file=True, control=True, custom=None, rota=None, time_rota=None):
        """
        初始化 MortalLog 实例。

        :param title: 日志的标题，默认为 None。
        :param file: 是否将日志输出到文件，默认为 True。
        :param control: 是否将日志输出到控制台，默认为 True。
        :param custom: 自定义日志配置，默认为 None。
        :param rota: 日志轮转配置，默认为 None。
        :param time_rota: 基于时间的日志轮转配置，默认为 None。
        """
        super().__init__(title, file, control, custom, rota, time_rota)

    def info(self, *message):
        """
        记录信息级别的日志。

        :param message: 要记录的信息，可以是多个参数。
        """
        self._info(*message)

    def debug(self, *message):
        """
        记录调试级别的日志。

        :param message: 要记录的调试信息，可以是多个参数。
        """
        self._debug(*message)

    def warning(self, *message):
        """
        记录警告级别的日志。

        :param message: 要记录的警告信息，可以是多个参数。
        """
        self._warning(*message)

    def error(self, *message):
        """
        记录错误级别的日志。

        :param message: 要记录的错误信息，可以是多个参数。
        """
        self._error(*message)

    def critical(self, *message):
        """
        记录严重错误级别的日志。

        :param message: 要记录的严重错误信息，可以是多个参数。
        """
        self._critical(*message)

    def close(self):
        """
        关闭日志记录器，释放相关资源。
        """
        self._close()

    def level(self, level):
        """
        设置日志记录器的全局日志级别。

        :param level: 日志级别，通常为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 等。
        """
        self._set_level(level)

    def file_level(self, level):
        """
        设置日志输出到文件的日志级别。

        :param level: 日志级别，通常为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 等。
        """
        self._set_file_level(level)

    def rota_level(self, level):
        """
        设置日志轮转的日志级别。

        :param level: 日志级别，通常为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 等。
        """
        self._set_rota_level(level)

    def time_rota_level(self, level):
        """
        设置基于时间的日志轮转的日志级别。

        :param level: 日志级别，通常为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 等。
        """
        self._set_time_rota_level(level)

    def control_level(self, level):
        """
        设置控制台输出的日志级别。

        :param level: 日志级别，通常为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 等。
        """
        self._set_control_level(level)
