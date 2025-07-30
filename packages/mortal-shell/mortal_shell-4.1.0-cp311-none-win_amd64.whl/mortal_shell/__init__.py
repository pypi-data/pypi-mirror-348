#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/4/10 15:25
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .shell_main import MortalShellMain


class MortalShell(MortalShellMain):
    """
    MortalShell 类继承自 MortalShellMain，用于管理与外部系统的连接和通信。

    Attributes:
        config: 配置信息，用于初始化连接。
    """

    def __init__(self, config):
        """
        初始化 MortalShell 实例。

        Args:
            config: 配置信息，用于初始化连接。
        """
        super().__init__(config)

    def connect(self):
        """
        建立与外部系统的连接。

        Returns:
            返回连接结果，通常为布尔值或连接对象。
        """
        return self._connect()

    def send(self, command):
        """
        发送命令到外部系统。

        Args:
            command: 要发送的命令字符串。
        """
        self._send(command)

    def send_command(self, command):
        """
        发送命令并返回执行结果。

        Args:
            command: 要发送的命令字符串。

        Returns:
            返回命令执行的结果。
        """
        return self._send_command(command)

    def close(self):
        """
        关闭与外部系统的连接。
        """
        self._close()
