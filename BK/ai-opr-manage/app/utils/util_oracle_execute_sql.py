# -*- coding: utf-8 -*-
from django.db import connections
from django.conf import settings


class OracleExecuteSQL:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self):
        self.dbname = 'oracle'
        self.cursor = connections[self.dbname].cursor()

    def fetchall_to_dict(self, sql, params=None):
        """
        返回全部数据
        :param sql: sql语句
        :param params: sql语句参数
        :return: 例如：[{"id": id, "username": 'username', "first_name": 'first_name'}]
        """
        cursor = self.cursor
        cursor.execute(sql, params)
        desc = cursor.description
        object_list = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return object_list

    def fetchone_to_dict(self, sql, params=None):
        """
        返回一行数据
        :param sql: sql语句
        :param params: sql语句参数
        :return: 例如：{"id": id, "username": 'username', "first_name": 'first_name'}
        """
        cursor = self.cursor
        cursor.execute(sql, params)
        desc = cursor.description
        row = dict(zip([col[0] for col in desc], cursor.fetchone()))
        return row

    def close(self):
        self.cursor.close()


def become_sql(table_name, keyword):
    table_name = "\""+table_name+"\""
    if keyword:
        sql = """
            select * from (
            select rownum as rn, t.* from "{table_name_}" t where rownum <= :max_size) 
            e where e.rn >= :min_size and regexp_like({keyword}, :val);""".format(table_name_=table_name,
                                                                                  keyword=keyword)
        count_sql = """select count(1) from "{table_name_}" where regexp_like({keyword}, :val);""".format(
            table_name_=table_name, keyword=keyword)
    else:
        sql = """
            select * from (
            select rownum as rn, t.* from {table_name_} t where rownum <= :max_size) 
            e where e.rn >= :min_size;""".format(table_name_=table_name)
        count_sql = """select count(1) from "{table_name_}";""".format(table_name_=table_name)
    return sql, count_sql


def splice_sql(table, limit, page, column="*", keywords=[]):
    """
    [{"key": "id", "value": 1, "condition": "="}]
    拼接sql 支持动态条件
    """
    table = get_table_name(table)
    start = limit * page
    end = limit * (page - 1)
    count_sql = "select count(1) as count from " + str(table) + " where 1=1 "
    sql = "SELECT " + str(column) + " FROM (SELECT ROWNUM AS rowno, t.* FROM " + str(
        table) + " t WHERE ROWNUM <= " + str(
        start) + ") table_alias WHERE table_alias.rowno >" + str(end)
    for item in keywords:
        cur_w = " and " + item.get("key") + " "
        value = item.get("value")
        if item.get('condition') == 'like':
            cur_w += "LIKE \'%" + str(value) + "%\'"
        elif item.get('condition') == 'in':
            v_str = ""
            for v in range(len(value)):
                if v == 0:
                    v_str += str(value[v])
                else:
                    v_str += "," + str(value[v])
            cur_w += "IN " + " (" + v_str + ")"
        else:
            if type(value).__name__ == 'str':
                value = "\'"+value+"\'"
            else:
                value = str(value)
            cur_w += item.get("condition") + " " + value
        sql += cur_w
        count_sql += cur_w
    return sql, count_sql


def get_table_name(table_name):
    data_base_name = settings.ORACLE_DATA_BASE_NAME
    if data_base_name:
        table_name = "\"" + data_base_name + "." + table_name + "\""
    else:
        table_name = "\"" + table_name + "\""
    return table_name


# oracle_execute_sql = OracleExecuteSQL()
