#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/17 10:11
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .curl_main import MortalCurlMain


class MortalCurl(MortalCurlMain):
    def to_dict(self, curl):
        """
        将 curl 命令转换为字典格式。

        :param curl: 需要转换的 curl 命令字符串。
        :return: 返回转换后的字典。
        """
        return self._to_dict(curl)

    def to_python(self, curl_path: str, file_path: str):
        """
        将 curl 命令转换为 Python 代码并保存到指定文件。

        :param curl_path: 包含 curl 命令的文件路径。
        :param file_path: 保存生成的 Python 代码的文件路径。
        """
        self._to_python(curl_path, file_path)

    def to_yaml(self, curl_path: str, file_path: str):
        """
        将 curl 命令转换为 YAML 格式并保存到指定文件。

        :param curl_path: 包含 curl 命令的文件路径。
        :param file_path: 保存生成的 YAML 文件路径。
        """
        self._to_yaml(curl_path, file_path)
