#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 16:51
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from typing import Dict, List, Optional, Any, Tuple
from weakref import proxy

from .var_main import MortalVarMain


class MortalVar(MortalVarMain):
    """
    MortalVar 类继承自 MortalVarMain，用于管理和操作变量集合。
    提供了添加、删除、设置、获取变量等操作。
    """

    def __init__(self, reprint: bool = False, inherit: bool = False, **kwargs: Any) -> None:
        """
        初始化 MortalVar 实例。

        :param reprint: 是否重新打印变量，默认为 False。
        :param inherit: 是否继承父类的变量，默认为 False。
        :param kwargs: 初始变量键值对。
        """
        self._set_class(MortalVar, reprint, inherit)
        self._mv_add(kwargs)

    def __enter__(self):
        return proxy(self)

    def __exit__(self, *args):
        self.__dict__.clear()

    def add(self, **kwargs: Any) -> None:
        """
        添加变量到当前实例。

        :param kwargs: 要添加的变量键值对。
        """
        self._mv_add(kwargs)

    def add_list(self, *args: Any) -> None:
        """
        添加多个变量到当前实例。

        :param args: 要添加的变量列表。
        """
        self._mv_add_list(args)

    def pop(self, name: str) -> None:
        """
        删除指定名称的变量。

        :param name: 要删除的变量名称。
        """
        self._mv_pop(name)

    def pops(self, *args: str) -> None:
        """
        删除多个指定名称的变量。

        :param args: 要删除的变量名称列表。
        """
        self._mv_pops(args)

    def set(self, name: str, value: Any, inherit: bool = False) -> None:
        """
        设置指定名称的变量值。

        :param name: 要设置的变量名称。
        :param value: 要设置的变量值。
        :param inherit: 是否继承父类的变量，默认为 False。
        """
        self._mv_set(name, value, inherit)

    def set_kwargs(self, **kwargs: Any) -> None:
        """
        批量设置变量值。

        :param kwargs: 要设置的变量键值对。
        """
        self._mv_set_kwargs(kwargs)

    def clear(self) -> None:
        """
        清除所有变量。
        """
        self._mv_clear()

    def get(self, key: Any, default: Any = None) -> Optional[Any]:
        """
        获取指定名称的变量值。

        :param key: 要获取的变量名称。
        :param default: 获取变量出错时，默认返回的值。
        :return: 返回变量值。
        """
        return self._mv_get(key, default)

    def keys(self) -> List[str]:
        """
        获取所有变量名称。

        :return: 返回所有变量名称的列表。
        """
        return self._mv_keys()

    def values(self) -> List[Any]:
        """
        获取所有变量值。

        :return: 返回所有变量值的列表。
        """
        return self._mv_values()

    def items(self) -> List[Tuple[str, Any]]:
        """
        获取所有变量名称和值的键值对。

        :return: 返回所有变量名称和值的键值对列表。
        """
        return self._mv_items()

    def todict(self, sort: bool = False) -> Dict[str, Any]:
        """
        将当前实例的变量转换为字典。

        :param sort: 是否对字典进行排序，默认为 False。
        :return: 返回包含所有变量的字典。
        """
        return self._mv_to_dict(sort)

    def to_params(self) -> str:
        """
        将当前实例的变量转换为参数字符串。

        :return: 返回参数字符串。
        """
        return self._mv_to_params()

    def to_string(self) -> str:
        """
        将当前实例的变量转换为字符串。

        :return: 返回变量字符串。
        """
        return self._mv_to_string()
