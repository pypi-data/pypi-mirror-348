# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:08
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .build_main import MortalBuildMain


class MortalBuild(MortalBuildMain):
    """
    MortalBuild 类继承自 MortalBuildMain，用于构建项目的配置和扩展模块。
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_config(self):
        """
        构建项目的配置。

        :return: 返回构建的配置信息。
        """
        return self._build_config()

    def build_wheel(self, config):
        """
        构建并生成项目的 wheel 包。

        :param config: 构建配置信息。
        :return: 返回生成的 wheel 包路径。
        """
        return self._build_wheel(config)

    def build_ext_wheel(self, config):
        """
        构建并生成扩展模块的 wheel 包。

        :param config: 构建配置信息。
        :return: 返回生成的 wheel 包路径。
        """
        return self._build_ext_wheel(config)

    def build_wheel_pypi(self, config):
        """
        构建并生成用于 PyPI 发布的扩展模块的 wheel 包。

        :param config: 构建配置信息。
        :return: 返回生成的 wheel 包路径。
        """
        return self._build_wheel_pypi(config)

    def build_ext_wheel_pypi(self, config):
        """
        构建并生成用于 PyPI 发布的扩展模块的 wheel 包。

        :param config: 构建配置信息。
        :return: 返回生成的 wheel 包路径。
        """
        return self._build_ext_wheel_pypi(config)
