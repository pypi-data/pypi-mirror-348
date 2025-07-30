#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2025/4/10 22:07
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalBases"]

import yaml

from .base_main import MortalBasesMain


class MortalBases(MortalBasesMain):
    """
    MortalBases 类继承自 MortalBasesMain，提供了一系列用于数据转换、字典操作、路径操作、可调用对象操作和时间处理的方法。
    """
    @classmethod
    def get_mortal_except(cls):
        """
        调用内部方法 `_get_mortal_except` 以获取异常装饰器。
        """
        return cls._get_mortal_except()

    @classmethod
    def undefined(cls):
        """
        返回一个未定义的值。

        :return: 返回一个未定义的值，具体类型和内容由 `_undefined()` 方法决定。
        """
        return cls._undefined()

    @classmethod
    def to_str(cls, obj, except_result="mortal_except_result"):
        """
        将对象转换为字符串。

        :param obj: 要转换的对象。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的字符串或默认值。
        """
        return cls._to_str(obj, except_result)

    @classmethod
    def to_int(cls, obj, ceil=False, floor=False, absolute=False, except_result="mortal_except_result"):
        """
        将对象转换为整数。

        :param obj: 要转换的对象。
        :param ceil: 是否向上取整，默认为 False。
        :param floor: 是否向下取整，默认为 False。
        :param absolute: 是否取绝对值，默认为 False。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的整数或默认值。
        """
        return cls._to_int(obj, ceil, floor, absolute, except_result)

    @classmethod
    def to_float(cls, obj, digits: int = 2, except_result="mortal_except_result"):
        """
        将对象转换为浮点数，并保留指定小数位数。

        :param obj: 要转换的对象。
        :param digits: 保留的小数位数，默认为 2。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的浮点数或默认值。
        """
        return cls._to_float(obj, digits, except_result)

    @classmethod
    def to_decimal(cls, obj, digits: int = 2, except_result="mortal_except_result"):
        """
        将对象转换为 Decimal 类型，并保留指定小数位数。

        :param obj: 要转换的对象。
        :param digits: 保留的小数位数，默认为 2。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的 Decimal 或默认值。
        """
        return cls._to_decimal(obj, digits, except_result)

    @classmethod
    def to_bool(cls, obj, except_result="mortal_except_result"):
        """
        将对象转换为布尔值。

        :param obj: 要转换的对象。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的布尔值或默认值。
        """
        return cls._to_bool(obj, except_result)

    @classmethod
    def list_diff(cls, left, right, except_result="mortal_except_result"):
        """
        计算两个列表的差集。

        :param left: 第一个列表。
        :param right: 第二个列表。
        :param except_result: 计算失败时返回的默认值，默认为 None。
        :return: 差集列表或默认值。
        """
        return cls._list_diff(left, right, except_result)

    @classmethod
    def list_set(cls, left, except_result="mortal_except_result"):
        """
        将列表转换为集合，去除重复元素。

        :param left: 要转换的列表。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的集合或默认值。
        """
        return cls._list_set(left, except_result)

    @classmethod
    def list_intersect(cls, left, right, except_result="mortal_except_result"):
        """
        计算两个列表的交集。

        :param left: 第一个列表。
        :param right: 第二个列表。
        :param except_result: 计算失败时返回的默认值，默认为 None。
        :return: 交集列表或默认值。
        """
        return cls._list_intersect(left, right, except_result)

    @classmethod
    def dict_find(cls, obj, path, except_result="mortal_except_result"):
        """
        在字典中查找指定路径的值。

        :param obj: 要查找的字典。
        :param path: 查找路径。
        :param except_result: 查找失败时返回的默认值，默认为 None。
        :return: 查找到的值或默认值。
        """
        return cls._dict_find(obj, path, except_result)

    @classmethod
    def dict_find_all(cls, obj, path, except_result="mortal_except_result"):
        """
        在字典中查找指定路径的所有值。

        :param obj: 要查找的字典。
        :param path: 查找路径。
        :param except_result: 查找失败时返回的默认值，默认为 None。
        :return: 查找到的所有值或默认值。
        """
        return cls._dict_find_all(obj, path, except_result)

    @classmethod
    def dict_update(cls, obj, path, value=None, except_result="mortal_except_result"):
        """
        更新字典中指定路径的值。

        :param obj: 要更新的字典。
        :param path: 更新路径。
        :param value: 要更新的值，默认为 None。
        :param except_result: 更新失败时返回的默认值，默认为 None。
        :return: 更新后的字典或默认值。
        """
        return cls._dict_update(obj, path, value, except_result)

    @classmethod
    def dict_delete(cls, obj, path, index=0, except_result="mortal_except_result"):
        """
        删除字典中指定路径的值。

        :param obj: 要删除的字典。
        :param path: 删除路径。
        :param index: 删除的索引，默认为 0。
        :param except_result: 删除失败时返回的默认值，默认为 None。
        :return: 删除后的字典或默认值。
        """
        return cls._dict_delete(obj, path, index, except_result)

    @classmethod
    def dict_read_yaml(cls, obj, mode='r', encoding="utf-8", loader=yaml.FullLoader, except_result="mortal_except_result"):
        """
        从 YAML 文件中读取字典。

        :param obj: YAML 文件路径或文件对象。
        :param mode: 文件打开模式，默认为 'r'。
        :param encoding: 文件编码，默认为 "utf-8"。
        :param loader: YAML 加载器，默认为 yaml.FullLoader。
        :param except_result: 读取失败时返回的默认值，默认为 None。
        :return: 读取到的字典或默认值。
        """
        return cls._dict_read_yaml(obj, mode, encoding, loader, except_result)

    @classmethod
    def dict_write_yaml(
            cls, obj, path, mode='w', default_style="", default_flow_style=False, canonical=False,
            indent=2, allow_unicode=True, encoding="utf-8", sort_keys=False, except_result="mortal_except_result"
    ):
        """
        将字典写入 YAML 文件。

        :param obj: 要写入的字典。
        :param path: 文件路径。
        :param mode: 文件打开模式，默认为 'w'。
        :param default_style: YAML 默认样式，默认为空字符串。
        :param default_flow_style: YAML 默认流样式，默认为 False。
        :param canonical: 是否使用规范格式，默认为 False。
        :param indent: 缩进空格数，默认为 2。
        :param allow_unicode: 是否允许 Unicode 字符，默认为 True。
        :param encoding: 文件编码，默认为 "utf-8"。
        :param sort_keys: 是否对键进行排序，默认为 False。
        :param except_result: 写入失败时返回的默认值，默认为 None。
        :return: 写入成功返回 True，失败返回默认值。
        """
        return cls._dict_write_yaml(
            obj, path, mode, default_style, default_flow_style, canonical, indent,
            allow_unicode, encoding, sort_keys, except_result
        )

    @classmethod
    def path_normal(cls, obj, except_result="mortal_except_result"):
        """
        规范化给定路径字符串，并处理可能的异常情况。

        :param obj: str, 需要规范化的路径字符串。
        :param except_result: 可选参数，指定在发生异常时返回的结果。默认为 None。
        :return: 规范化后的路径字符串。如果发生异常，则返回 `except_result` 指定的值。
        """
        return cls._path_normal(obj, except_result)

    @classmethod
    def path_exists(cls, obj, except_result="mortal_except_result"):
        """
        检查路径是否存在。

        :param obj: 要检查的路径。
        :param except_result: 检查失败时返回的默认值，默认为 None。
        :return: 路径存在返回 True，否则返回默认值。
        """
        return cls._path_exists(obj, except_result)

    @classmethod
    def path_file(cls, obj, except_result="mortal_except_result"):
        """
        检查路径是否为文件。

        :param obj: 要检查的路径。
        :param except_result: 检查失败时返回的默认值，默认为 None。
        :return: 路径为文件返回 True，否则返回默认值。
        """
        return cls._path_file(obj, except_result)

    @classmethod
    def path_dir(cls, obj, except_result="mortal_except_result"):
        """
        检查路径是否为目录。

        :param obj: 要检查的路径。
        :param except_result: 检查失败时返回的默认值，默认为 None。
        :return: 路径为目录返回 True，否则返回默认值。
        """
        return cls._path_dir(obj, except_result)

    @classmethod
    def path_delete(cls, obj, except_result="mortal_except_result"):
        """
        删除指定路径。

        :param obj: 要删除的路径。
        :param except_result: 删除失败时返回的默认值，默认为 None。
        :return: 删除成功返回 True，失败返回默认值。
        """
        return cls._path_delete(obj, except_result)

    @classmethod
    def path_copy(cls, src_obj, tar_obj, except_result="mortal_except_result"):
        """
        复制文件或目录。

        :param src_obj: 源路径。
        :param tar_obj: 目标路径。
        :param except_result: 复制失败时返回的默认值，默认为 None。
        :return: 复制成功返回 True，失败返回默认值。
        """
        return cls._path_copy(src_obj, tar_obj, except_result)

    @classmethod
    def path_move(cls, src_obj, tar_obj, except_result="mortal_except_result"):
        """
        移动文件或目录。

        :param src_obj: 源路径。
        :param tar_obj: 目标路径。
        :param except_result: 移动失败时返回的默认值，默认为 None。
        :return: 移动成功返回 True，失败返回默认值。
        """
        return cls._path_move(src_obj, tar_obj, except_result)

    @classmethod
    def path_read(cls, obj, mode='r', encoding=None, except_result="mortal_except_result"):
        """
        读取文件内容。

        :param obj: 文件路径。
        :param mode: 文件打开模式，默认为 'r'。
        :param encoding: 文件编码，默认为 None。
        :param except_result: 读取失败时返回的默认值，默认为 None。
        :return: 文件内容或默认值。
        """
        return cls._path_read(obj, mode, encoding, except_result)

    @classmethod
    def path_readline(cls, obj, mode='r', encoding=None, except_result="mortal_except_result"):
        """
        读取文件的一行内容。

        :param obj: 文件路径。
        :param mode: 文件打开模式，默认为 'r'。
        :param encoding: 文件编码，默认为 None。
        :param except_result: 读取失败时返回的默认值，默认为 None。
        :return: 文件的一行内容或默认值。
        """
        return cls._path_readline(obj, mode, encoding, except_result)

    @classmethod
    def path_readlines(cls, obj, mode='r', encoding=None, except_result="mortal_except_result"):
        """
        读取文件的所有行内容。

        :param obj: 文件路径。
        :param mode: 文件打开模式，默认为 'r'。
        :param encoding: 文件编码，默认为 None。
        :param except_result: 读取失败时返回的默认值，默认为 None。
        :return: 文件的所有行内容或默认值。
        """
        return cls._path_readlines(obj, mode, encoding, except_result)

    @classmethod
    def path_write(cls, obj, mode='w', encoding=None, except_result="mortal_except_result"):
        """
        向文件写入内容。

        :param obj: 文件路径。
        :param mode: 文件打开模式，默认为 'w'。
        :param encoding: 文件编码，默认为 None。
        :param except_result: 写入失败时返回的默认值，默认为 None。
        :return: 写入成功返回 True，失败返回默认值。
        """
        return cls._path_write(obj, mode, encoding, except_result)

    @classmethod
    def path_writelines(cls, obj, mode='w', encoding=None, except_result="mortal_except_result"):
        """
        向文件写入多行内容。

        :param obj: 文件路径。
        :param mode: 文件打开模式，默认为 'w'。
        :param encoding: 文件编码，默认为 None。
        :param except_result: 写入失败时返回的默认值，默认为 None。
        :return: 写入成功返回 True，失败返回默认值。
        """
        return cls._path_writelines(obj, mode, encoding, except_result)

    @classmethod
    def path_file_list(cls, obj, except_result="mortal_except_result"):
        """
        获取目录下的文件列表。

        :param obj: 目录路径。
        :param except_result: 获取失败时返回的默认值，默认为 None。
        :return: 文件列表或默认值。
        """
        return cls._path_file_list(obj, except_result)

    @classmethod
    def path_file_dict(cls, obj, dirs=None, skip_dir=None, skip_file=None, except_result="mortal_except_result"):
        """
        获取目录下的文件字典。

        :param obj: 目录路径。
        :param dirs: 是否包含子目录，默认为 None。
        :param skip_dir: 跳过的目录，默认为 None。
        :param skip_file: 跳过的文件，默认为 None。
        :param except_result: 获取失败时返回的默认值，默认为 None。
        :return: 文件字典或默认值。
        """
        return cls._path_file_dict(obj, dirs, skip_dir, skip_file, except_result)

    @classmethod
    def callable_name(cls, obj, except_result="mortal_except_result"):
        """
        获取可调用对象的名称。

        :param obj: 可调用对象。
        :param except_result: 获取失败时返回的默认值，默认为 None。
        :return: 可调用对象的名称或默认值。
        """
        return cls._callable_name(obj, except_result)

    @classmethod
    def callable_ref(cls, obj, except_result="mortal_except_result"):
        """
        获取可调用对象的引用。

        :param obj: 可调用对象。
        :param except_result: 获取失败时返回的默认值，默认为 None。
        :return: 可调用对象的引用或默认值。
        """
        return cls._callable_ref(obj, except_result)

    @classmethod
    def callable_obj(cls, ref, except_result="mortal_except_result"):
        """
        通过引用获取可调用对象。

        :param ref: 可调用对象的引用。
        :param except_result: 获取失败时返回的默认值，默认为 None。
        :return: 可调用对象或默认值。
        """
        return cls._callable_obj(ref, except_result)

    @classmethod
    def callable_convert_obj(cls, obj, except_result="mortal_except_result"):
        """
        将对象转换为可调用对象。

        :param obj: 要转换的对象。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的可调用对象或默认值。
        """
        return cls._callable_convert_obj(obj, except_result)

    @classmethod
    def callable_check_args(cls, func, args, kwargs):
        """
        检查可调用对象的参数是否匹配。

        :param func: 可调用对象。
        :param args: 位置参数。
        :param kwargs: 关键字参数。
        :return: 参数匹配返回 True，否则返回 False。
        """
        return cls._callable_check_args(func, args, kwargs)

    @classmethod
    def callable_coroutine(cls, obj, except_result="mortal_except_result"):
        """
        将对象转换为协程对象。

        :param obj: 要转换的对象。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的协程对象或默认值。
        """
        return cls._callable_coroutine(obj, except_result)

    @classmethod
    def time_datetime(cls, obj, tz=None, except_result="mortal_except_result"):
        """
        将对象转换为 datetime 对象。可以通过 `tz` 参数指定时区信息。

        :param obj: 要转换的对象，可以是字符串、时间戳或其他可转换为 `datetime` 的类型。
        :param tz: 时区信息，用于指定转换后的 `datetime` 对象的时区，默认为 None。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的 `datetime` 对象，如果转换失败则返回 `except_result`。
        """
        return cls._time_datetime(obj, tz, except_result)

    @classmethod
    def time_timestamp(cls, obj, tz=None, except_result="mortal_except_result"):
        """
        将对象转换为时间戳。

        :param obj: 要转换的对象。
        :param tz: 时区信息，用于指定转换后的 `datetime` 对象的时区，默认为 None。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的时间戳或默认值。
        """
        return cls._time_timestamp(obj, tz, except_result)

    @classmethod
    def time_ceil(cls, obj, except_result="mortal_except_result"):
        """
        将时间对象向上取整。

        :param obj: 要取整的时间对象。
        :param except_result: 取整失败时返回的默认值，默认为 None。
        :return: 取整后的时间对象或默认值。
        """
        return cls._time_ceil(obj, except_result)

    @classmethod
    def time_date(cls, obj, except_result="mortal_except_result"):
        """
        将对象转换为日期对象。

        :param obj: 要转换的对象。
        :param except_result: 转换失败时返回的默认值，默认为 None。
        :return: 转换后的日期对象或默认值。
        """
        return cls._time_date(obj, except_result)

    @classmethod
    def time_str(cls, obj, fmt="%Y-%m-%d %H:%M:%S.%f", except_result="mortal_except_result"):
        """
        将时间对象转换为指定格式的字符串。

        :param obj: 时间对象，可以是datetime、timestamp等。
        :param fmt: 时间格式化字符串，默认为"%Y-%m-%d %H:%M:%S.%f"。
        :param except_result: 如果转换失败，返回的默认值。
        :return: 格式化后的时间字符串，如果转换失败则返回except_result。
        """
        return cls._time_str(obj, fmt, except_result)

    @classmethod
    def time_timezone(cls, obj, except_result="mortal_except_result"):
        """
        获取时间对象的时区信息。

        :param obj: 时间对象，可以是datetime、timestamp等。
        :param except_result: 如果获取时区信息失败，返回的默认值。
        :return: 时区信息，如果获取失败则返回except_result。
        """
        return cls._time_timezone(obj, except_result)

    @classmethod
    def time_seconds(cls, obj, except_result="mortal_except_result"):
        """
        将时间对象转换为秒数。

        :param obj: 时间对象，可以是datetime、timestamp等。
        :param except_result: 如果转换失败，返回的默认值。
        :return: 时间对象的秒数表示，如果转换失败则返回except_result。
        """
        return cls._time_seconds(obj, except_result)

    @classmethod
    def time_normalize(cls, obj):
        """
        规范化时间对象，去除时区信息。

        :param obj: 时间对象，可以是datetime、timestamp等。
        :return: 规范化后的datetime对象。
        """
        return cls._time_normalize(obj)

    @classmethod
    def time_localize(cls, obj, tz):
        """
        将时间对象本地化到指定时区。

        :param obj: 时间对象，可以是datetime、timestamp等。
        :param tz: 目标时区。
        :return: 本地化后的datetime对象。
        """
        return cls._time_localize(obj, tz)
