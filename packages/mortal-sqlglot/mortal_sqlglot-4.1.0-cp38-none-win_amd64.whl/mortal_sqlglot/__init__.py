#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2025/2/19 16:38
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py.py
"""
from .sqlglot_main import MortalSQLGlotMain


"""
先查select和from，分别设置id，
查询from中的表设置id，如果有子查询，递归追溯绑定源id，
查询select中的字段设置id，并单独存储，如果有子查询、函数等（排除条件），递归追溯绑定源id，
用单独存储的字段，按id追溯源头，直到绑定源id为空
"""


class MortalSQLGlot(MortalSQLGlotMain):
    """
    MortalSQLGlot 类继承自 MortalSQLGlotMain，用于处理 SQL 语句的格式化和解析。
    """

    def __init__(self, *args, **kwargs):
        """
        初始化 MortalSQLGlot 类实例。

        Args:
            *args: 可变位置参数，传递给父类的初始化方法。
            **kwargs: 可变关键字参数，传递给父类的初始化方法。
        """
        super().__init__(*args, **kwargs)

    def format(self, sql):
        """
        格式化 SQL 语句。

        Args:
            sql (str): 需要格式化的 SQL 语句。

        Returns:
            str: 格式化后的 SQL 语句。
        """
        return self._format(sql)

    def parse(self, sql, dialect="mysql", callback="print"):
        """
        解析 SQL 语句。

        Args:
            sql (str): 需要解析的 SQL 语句。
            dialect (str, optional): SQL 方言，默认为 "mysql"。
            callback (str, optional): 回调函数名，默认为 "print"，可选["mortal", "normal", "dataframe", "sql", "table"]。

        Returns:
            Any: 解析后的结果，具体类型取决于回调函数的实现。
        """
        return self._parse(sql, dialect, callback)
