# -*- coding: utf-8 -*-
from django.db import connections


class OracleExecuteSQL:
    def __init__(self):
        self.dbname = 'oracle'

    def fetchall_to_dict(self, sql, params=None):
        """
        返回全部数据
        :param sql: sql语句
        :param params: sql语句参数
        :param db: Django数据库名
        :return: 例如：[{"id": id, "username": 'username', "first_name": 'first_name'}]
        """
        cursor = connections[self.dbname].cursor()
        cursor.execute(sql, params)
        desc = cursor.description
        object_list = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return object_list


oracle_execute_sql = OracleExecuteSQL()
