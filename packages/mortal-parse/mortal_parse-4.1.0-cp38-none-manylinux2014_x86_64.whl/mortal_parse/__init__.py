#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 13:55
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .sqlparse_main import MortalParseMain


class MortalParse(MortalParseMain):
    """
    MortalParse 类继承自 MortalParseMain，用于处理 SQL 语句的解析和格式化功能。
    """

    def re_hint(self, sql):
        """
        对给定的 SQL 语句进行格式化处理。

        :param sql: 需要处理的 SQL 语句，类型为字符串。
        :return: 返回处理后的 SQL 格式化信息，类型为字符串。
        """
        return self._re_hint(sql)

    def parse_sql(self, sql):
        """
        对给定的 SQL 语句进行解析。

        :param sql: 需要解析的 SQL 语句，类型为字符串。
        :return: 返回解析后的 SQL 信息，类型为字符串。
        """
        return self._parse_sql(sql)
