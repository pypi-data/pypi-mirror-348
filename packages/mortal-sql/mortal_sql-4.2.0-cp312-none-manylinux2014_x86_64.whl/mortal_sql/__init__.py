#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 11:30
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalSQL", "MortalExecute"]
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from .orm_main import MortalSQLMain
from .execute_main import MortalExecuteMain


class MortalSQL(MortalSQLMain):
    """
    MortalSQL 类继承自 MortalSQLMain，用于管理与数据库的交互操作。
    """

    def __init__(self, config):
        """
        初始化 MortalSQL 实例。

        :param config: 数据库配置信息。
        """
        self._mortal_config = config
        super().__init__(config)

    @contextmanager
    def sessionmaker(self, logging_token=None):
        session = self.session(logging_token)
        try:
            yield session
        finally:
            self.close_session(session)

    def session(self, logging_token=None):
        """
        创建一个数据库会话。

        :param logging_token: 可选的日志记录令牌。
        :return: 返回创建的数据库会话。
        """
        return self._create_session(logging_token)

    def close_session(self, session):
        """
        关闭指定的数据库会话。

        :param session: 要关闭的数据库会话。
        :return: 无返回值。
        """
        return self._close_session(session)

    def get_table(self, table):
        """
        获取指定表对象。

        :param table: 表名。
        :return: 返回表对象。
        """
        return self._get_table(table)

    def alias(self, table):
        """
        为指定表创建别名。

        :param table: 表名。
        :return: 返回表的别名对象。
        """
        return self._alias(table)

    def column(self, table, column):
        """
        获取指定表的列对象。

        :param table: 表名。
        :param column: 列名。
        :return: 返回列对象。
        """
        return self._column(table, column)

    def get_create_tables_data(self, schema, table):
        """
        获取创建表所需的数据。

        :param schema: 数据库模式。
        :param table: 表名。
        :return: 返回创建表所需的数据。
        """
        return self._get_create_tables_data(schema, table)

    def create_orm(self, read_tables=None, create_tables=None, key_long=False):
        """
        创建 ORM 映射。

        :param read_tables: 要读取的表列表。
        :param create_tables: 要创建的表列表。
        :param key_long: 是否使用长键。
        :return: 无返回值。
        """
        self._create_orm(read_tables, create_tables, key_long)

    def create_models(self, outfile="./test_models.py", tables=None, schemas=None, options=None):
        """
        创建模型文件。

        :param outfile: 输出文件路径。
        :param tables: 要创建模型的表列表。
        :param schemas: 数据库模式列表。
        :param options: 其他选项。
        :return: 无返回值。
        """
        self._create_models(outfile, tables, schemas, options)

    def show_column(self, table_name):
        """
        显示指定表的列信息。

        :param table_name: 表名。
        :return: 返回列信息。
        """
        return self._show_column(table_name)

    def get_columns(self, table_name):
        """
        获取指定表的所有列。

        :param table_name: 表名。
        :return: 返回列列表。
        """
        return self._get_columns(table_name)

    def get_tables(self):
        """
        获取数据库中的所有表。

        :return: 返回表列表。
        """
        return self._get_tables()

    def drop(self, table_name):
        """
        删除指定表。

        :param table_name: 表名。
        :return: 无返回值。
        """
        self._drop(table_name)

    def drop_all(self):
        """
        删除数据库中的所有表。

        :return: 无返回值。
        """
        return self._drop_all()

    def query_to_sql(self, query):
        """
        将查询对象转换为 SQL 语句。

        :param query: 查询对象。
        :return: 返回 SQL 语句。
        """
        return self._query_to_sql(query)

    def to_dict(self, result):
        """
        将查询结果转换为字典。

        :param result: 查询结果。
        :return: 返回字典形式的结果。
        """
        return self._to_dict(result)

    def query(self, sql, args=None, kwargs=None):
        """
        执行 SQL 查询。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :return: 返回查询结果。
        """
        return self._query(sql, args, kwargs)

    def execute(self, sql, args=None, kwargs=None):
        """
        执行 SQL 语句。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :return: 无返回值。
        """
        self._execute(sql, args, kwargs)

    def fetchone(self, sql, args=None, kwargs=None):
        """
        获取查询结果的第一行。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :return: 返回查询结果的第一行。
        """
        return self._fetchone(sql, args, kwargs)

    def fetchmany(self, sql, args=None, kwargs=None, many=1):
        """
        获取查询结果的多行。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :param many: 要获取的行数。
        :return: 返回查询结果的多行。
        """
        return self._fetchmany(sql, args, kwargs, many)

    def fetchall(self, sql, args=None, kwargs=None):
        """
        获取查询结果的所有行。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :return: 返回查询结果的所有行。
        """
        return self._fetchall(sql, args, kwargs)

    def read_sql(self, sql, coerce_float=False, **kwargs):
        """
        读取 SQL 查询结果。

        :param sql: SQL 语句。
        :param coerce_float: 是否将数值强制转换为浮点数。
        :param kwargs: 其他关键字参数。
        :return: 返回查询结果。
        """
        return self._read_sql(sql, coerce_float, **kwargs)

    def read_sql_query(self, query, coerce_float=False, **kwargs):
        """
        读取 SQL 查询结果。

        :param query: SQL 查询语句。
        :param coerce_float: 是否将数值强制转换为浮点数。
        :param kwargs: 其他关键字参数。
        :return: 返回查询结果。
        """
        return self._read_sql_query(query, coerce_float, **kwargs)

    def read_sql_table(self, table_name, coerce_float=False, **kwargs):
        """
        读取指定表的数据。

        :param table_name: 表名。
        :param coerce_float: 是否将数值强制转换为浮点数。
        :param kwargs: 其他关键字参数。
        :return: 返回表数据。
        """
        return self._read_sql_table(table_name, coerce_float, **kwargs)

    def to_sql(self, data, table_name, if_exists='append'):
        """
        将数据写入数据库表。

        :param data: 要写入的数据。
        :param table_name: 表名。
        :param if_exists: 如果表已存在时的处理方式。
        :return: 无返回值。
        """
        self._to_sql(data, table_name, if_exists)

    def mortal_execute(self):
        """
        创建一个 MortalExecute 实例。

        :return: 返回 MortalExecute 实例。
        """
        return MortalExecute(self._mortal_config)

    def close(self):
        """
        关闭数据库连接。

        :return: 无返回值。
        """
        self._close()

    def data_sync(self, name, path, max_overflow=10, skip_dir=None):
        """
        同步数据到指定路径。

        :param name: 数据名称。
        :param path: 目标路径。
        :param max_overflow: 最大溢出量。
        :param skip_dir: 要跳过的目录。
        :return: 无返回值。
        """
        self._data_sync(name, path, max_overflow, skip_dir)


class MortalExecute(MortalExecuteMain):
    """
    MortalExecute 类继承自 MortalExecuteMain，用于执行数据库操作。
    """

    def __init__(self, config):
        """
        初始化 MortalExecute 实例。

        :param config: 数据库配置信息。
        """
        super().__init__(config)

    def execute(self, sql, args=None, kwargs=None):
        """
        执行 SQL 语句。

        :param sql: SQL 语句。
        :param args: SQL 参数。
        :param kwargs: SQL 关键字参数。
        :return: 无返回值。
        """
        self._execute(sql, args, kwargs)

    def commit(self):
        """
        提交事务。

        :return: 无返回值。
        """
        self._commit()

    def rollback(self):
        """
        回滚事务。

        :return: 无返回值。
        """
        self._rollback()

    def close(self):
        """
        关闭数据库连接。

        :return: 无返回值。
        """
        self._close()
