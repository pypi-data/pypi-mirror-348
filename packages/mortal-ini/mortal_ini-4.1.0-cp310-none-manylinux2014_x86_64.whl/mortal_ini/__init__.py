#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/18 10:04
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .ini_main import MortalIniMain


class MortalIni(MortalIniMain):
    def __init__(self, path):
        """
        初始化 MortalIni 类。

        :param path: INI 文件的路径。
        """
        super().__init__(path)

    def get(self, section, option):
        """
        获取指定 section 和 option 的值。

        :param section: INI 文件中的 section 名称。
        :param option: section 中的 option 名称。
        :return: 返回指定 option 的值。
        """
        return self._get(section, option)

    def get_option(self, section):
        """
        获取指定 section 中的所有 option 及其值。

        :param section: INI 文件中的 section 名称。
        :return: 返回一个包含所有 option 及其值的字典。
        """
        return self._get_option(section)

    def get_all(self):
        """
        获取 INI 文件中所有 section 及其 option 和值。

        :return: 返回一个包含所有 section 及其 option 和值的字典。
        """
        return self._get_all()

    def set(self, section, option, value, save=True):
        """
        设置指定 section 和 option 的值。

        :param section: INI 文件中的 section 名称。
        :param option: section 中的 option 名称。
        :param value: 要设置的值。
        :param save: 是否立即保存更改，默认为 True。
        """
        self._set(section, option, value, save)

    def set_option(self, section, option_dict, save=True):
        """
        设置指定 section 中的多个 option 及其值。

        :param section: INI 文件中的 section 名称。
        :param option_dict: 包含 option 及其值的字典。
        :param save: 是否立即保存更改，默认为 True。
        """
        self._set_option(section, option_dict, save)

    def set_all(self, section_dict, save=True):
        """
        设置 INI 文件中多个 section 及其 option 和值。

        :param section_dict: 包含 section 及其 option 和值的字典。
        :param save: 是否立即保存更改，默认为 True。
        """
        self._set_all(section_dict, save)

    def sections(self):
        """
        获取 INI 文件中所有的 section 名称。

        :return: 返回一个包含所有 section 名称的列表。
        """
        return self._sections()

    def options(self, section):
        """
        获取指定 section 中的所有 option 名称。

        :param section: INI 文件中的 section 名称。
        :return: 返回一个包含所有 option 名称的列表。
        """
        return self._options(section)

    def remove_section(self, section, save=True):
        """
        移除指定的 section。

        :param section: 要移除的 section 名称。
        :param save: 是否立即保存更改，默认为 True。
        """
        self._remove_section(section, save)

    def remove_option(self, section, options, save=True):
        """
        移除指定 section 中的 option。

        :param section: section 名称。
        :param options: 要移除的 option 名称。
        :param save: 是否立即保存更改，默认为 True。
        """
        self._remove_option(section, options, save)

    def has_section(self, section):
        """
        检查 INI 文件中是否存在指定的 section。

        :param section: 要检查的 section 名称。
        :return: 如果存在返回 True，否则返回 False。
        """
        return self._has_section(section)

    def has_option(self, section, option):
        """
        检查指定 section 中是否存在指定的 option。

        :param section: section 名称。
        :param option: 要检查的 option 名称。
        :return: 如果存在返回 True，否则返回 False。
        """
        return self._has_option(section, option)
