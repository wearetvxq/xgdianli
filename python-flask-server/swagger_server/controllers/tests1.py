# -*- coding: UTF-8 -*-
import connexion
from datetime import date
from typing import List, Dict
from six import iteritems
from swagger_server.utitl.mysqlset import MySQL
from swagger_server.utitl.common import com
from flask import json, jsonify
from flask import Response
import datetime
import calendar
import itsdangerous
import time


def insert_met_reader():
    mysql = MySQL(2)
    mysql.mysql_connect()

    sql_0 = "SELECT sta_num,met_reader FROM source_sta_meter WHERE met_reader !='' GROUP BY sta_num"
    print('---sql_0--', sql_0)
    result_0 = mysql.query(sql_0)
    print('result_0:', result_0)
    print('---result_0--', len(result_0))
    for i in range(len(result_0)):
        print('i--:', i)
        sql = """insert into basic_reader_list(sta_no, met_reader)VALUES('{0}', '{1}')""".format(result_0[i][0], result_0[i][1])
        print('====sql:==', sql)
        mysql.executesql(sql)
        mysql.commitdata()

    mysql.mysql_close()
    return 1

if __name__ == '__main__':
    # token = get_authtoken()
    # print('token:', token)
    a = insert_met_reader()