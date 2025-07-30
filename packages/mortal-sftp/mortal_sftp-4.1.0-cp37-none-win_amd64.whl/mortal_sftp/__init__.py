#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 11:03
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .sftp_main import MortalSFTPMain


class MortalSFTP(MortalSFTPMain):
    """
    MortalSFTP 类继承自 MortalSFTPMain，提供了对 SFTP 操作的封装。
    """
    def __init__(self, config):
        """
        初始化 MortalSFTP 实例。

        :param config: 配置信息，用于初始化 SFTP 连接。
        """
        super().__init__(config)

    def connect(self):
        """
        建立 SFTP 连接。
        """
        self._connect()

    def remove(self, path):
        """
        删除指定路径的文件或目录。

        :param path: 要删除的文件或目录的路径。
        :return: 删除操作的结果。
        """
        return self._remove(path)

    def rename(self, ole_path, new_path):
        """
        重命名文件或目录。

        :param ole_path: 原文件或目录的路径。
        :param new_path: 新文件或目录的路径。
        :return: 重命名操作的结果。
        """
        return self._rename(ole_path, new_path)

    def posix_rename(self, ole_path, new_path):
        """
        使用 POSIX 标准重命名文件或目录。

        :param ole_path: 原文件或目录的路径。
        :param new_path: 新文件或目录的路径。
        :return: 重命名操作的结果。
        """
        return self._posix_rename(ole_path, new_path)

    def mkdir(self, path):
        """
        创建目录。

        :param path: 要创建的目录路径。
        :return: 创建目录操作的结果。
        """
        return self._mkdir(path)

    def rmdir(self, path):
        """
        删除目录。

        :param path: 要删除的目录路径。
        :return: 删除目录操作的结果。
        """
        return self._rmdir(path)

    def stat(self, file_path):
        """
        获取文件或目录的状态信息。

        :param file_path: 要获取状态的文件或目录路径。
        :return: 文件或目录的状态信息。
        """
        return self._stat(file_path)

    def normalize(self, path):
        """
        规范化路径。

        :param path: 要规范化的路径。
        :return: 规范化后的路径。
        """
        return self._normalize(path)

    def chdir(self, path):
        """
        更改当前工作目录。

        :param path: 要切换到的目录路径。
        :return: 更改目录操作的结果。
        """
        return self._chdir(path)

    def upload(self, src_file, dsc_path):
        """
        上传文件到远程服务器。

        :param src_file: 本地文件路径。
        :param dsc_path: 远程服务器目标路径。
        :return: 上传操作的结果。
        """
        return self._upload(src_file, dsc_path)

    def download(self, src_file, dsc_path):
        """
        从远程服务器下载文件。

        :param src_file: 远程服务器文件路径。
        :param dsc_path: 本地目标路径。
        :return: 下载操作的结果。
        """
        return self._download(src_file, dsc_path)

    def close(self):
        """
        关闭 SFTP 连接。
        """
        self._close()
