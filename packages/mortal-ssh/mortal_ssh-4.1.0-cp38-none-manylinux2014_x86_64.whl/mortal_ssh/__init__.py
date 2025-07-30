#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 15:34
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .ssh_main import MortalSSHMain


class MortalSSH(MortalSSHMain):
    """
    MortalSSH 类继承自 MortalSSHMain，用于管理与 SSH 连接相关的操作。

    Attributes:
        config: 配置信息，用于初始化 SSH 连接。
    """

    def __init__(self, config):
        """
        初始化 MortalSSH 实例。

        Args:
            config: 配置信息，用于初始化 SSH 连接。
        """
        super().__init__(config)

    def connect(self):
        """
        建立 SSH 连接。

        Returns:
            返回连接结果，通常是一个表示连接状态的布尔值或连接对象。
        """
        return self._connect()

    def close(self):
        """
        关闭 SSH 连接。
        """
        self._close()
