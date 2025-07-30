#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 10:14
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .redis_main import MortalRedisMain


class MortalRedis(MortalRedisMain):
    """
    MortalRedis 类继承自 MortalRedisMain，提供了对 Redis 数据库的基本操作封装。
    """
    def __init__(self, config):
        """
        初始化 MortalRedis 实例。

        :param config: 配置信息，用于初始化 Redis 连接。
        """
        super().__init__(config)

    def close(self):
        """
        关闭 Redis 连接。
        """
        self._close()

    def close_db(self, db=0):
        """
        关闭指定数据库的 Redis 连接。

        :param db: 数据库编号，默认为 0。
        """
        self._close_db(db)

    def set(self, key, value, db=0):
        """
        在指定数据库中设置键值对。

        :param key: 键名。
        :param value: 值。
        :param db: 数据库编号，默认为 0。
        """
        self._set(key, value, db)

    def get(self, key, db=0):
        """
        从指定数据库中获取键对应的值。

        :param key: 键名。
        :param db: 数据库编号，默认为 0。
        :return: 键对应的值。
        """
        return self._get(key, db)

    def set_list(self, key, value: list, db=0):
        """
        在指定数据库中设置列表类型的键值对。

        :param key: 键名。
        :param value: 列表类型的值。
        :param db: 数据库编号，默认为 0。
        """
        self._set_list(key, value, db)

    def get_list(self, key, db=0):
        """
        从指定数据库中获取列表类型的键对应的值。

        :param key: 键名。
        :param db: 数据库编号，默认为 0。
        :return: 列表类型的值。
        """
        return self._get_list(key, db)

    def set_dict(self, key, value: dict, db=0):
        """
        在指定数据库中设置字典类型的键值对。

        :param key: 键名。
        :param value: 字典类型的值。
        :param db: 数据库编号，默认为 0。
        """
        self._set_dict(key, value, db)

    def get_dict(self, key, db=0):
        """
        从指定数据库中获取字典类型的键对应的值。

        :param key: 键名。
        :param db: 数据库编号，默认为 0。
        :return: 字典类型的值。
        """
        return self._get_dict(key, db)

    def delete(self, key, db=0):
        """
        从指定数据库中删除键。

        :param key: 键名。
        :param db: 数据库编号，默认为 0。
        :return: 删除操作的结果。
        """
        return self._delete(key, db)

    def get_size(self, db=0):
        """
        获取指定数据库的大小。

        :param db: 数据库编号，默认为 0。
        :return: 数据库的大小。
        """
        return self._get_size(db)

    def pipeline(self, pipe_dict: dict, db=0):
        """
        在指定数据库中执行管道操作。

        :param pipe_dict: 包含管道操作的字典。
        :param db: 数据库编号，默认为 0。
        """
        self._pipeline(pipe_dict, db)

    def keys(self, pattern, db=0):
        """
        在指定数据库中查找匹配模式的键。

        :param pattern: 匹配模式。
        :param db: 数据库编号，默认为 0。
        :return: 匹配的键列表。
        """
        return self._keys(pattern, db)
