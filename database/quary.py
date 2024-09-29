# -*- coding: utf-8 -*-
# @Author  : JiaWei Liu
# @Time    : 2024/9/26 08:52
# @Function: 输入某个字符串命令，进行数据库查询

from pymysql import *

conn = connect(host='localhost',user='root',password='123456',database='face_db',port=3306)
cursor = conn.cursor()


def querys(sql,params,type='no_select'):
    params = tuple(params)
    cursor.execute(sql,params)
    conn.ping(reconnect=True)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'

