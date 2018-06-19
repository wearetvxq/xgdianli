# -*- coding: UTF-8 -*-
import connexion
from datetime import date
from typing import List, Dict
from six import iteritems
from swagger_server.utitl.mysqlset import MySQL
from swagger_server.utitl.common import com
from flask import json, jsonify
from flask import Response
import datetime,time,hashlib
import calendar
import itsdangerous
import time

# ##############################################
#                                              #
#                  test页面                    #
#                                              #
# ##############################################


class test_page:
    def hello(self, arg1='', arg2=[]):
        resultdict = {}
        mysql = MySQL(2)
        mysql.mysql_connect()
        test = com.zzy_test(self, arg2)
        resultdict['test'] = test
        mysql.mysql_close()
        reps = jsonify(resultdict)
        reps.headers["Access-Control-Allow-Origin"] = "*"
        return reps

    def hello1(self, list_test=[]):
        return 1


test_page_object = test_page()


def test(arg1='', arg2=1):
    reps = jsonify("test")
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


def function_1():
    times = str(int(time.time()))
    noncestr = 'flyminer123'
    text = 'jsapi_ticket=kgt8ON7yVITDhtdwci0qeYVyQ6vRX7VgFbWTv_c8scjtzGyd5EwfQ_kKLxzAkOBj2He8544brrm4g7z-LwbbLw&noncestr={}&timestamp={}&url=http://wx.caicool.cc/inbound'.format(
        noncestr, times)

    code = hashlib.sha1(text.encode('UTF-8')).hexdigest()

    msg = {"code": 0, 'msg': 'success', "result": [{"code": code, "times": int(times), "noncestr": noncestr}]}
    return msg

import itsdangerous
import time
def get_authtoken():
    s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key='4fba6786c7e54b00976270ab52f75dbe')
    timestamp = time.time()
    return s.dumps({'user_id': 'mo', 'user_role': 'common user', 'iat': timestamp})


def tttt():
    tt = []
    tt_1 = [{'name': '波动异常0', 'xAxis': '2017-10'}, {'xAxis': '2017-20'}]
    tt_2 = [{'name': '波动异常1', 'xAxis': '2017-11'}, {'xAxis': '2017-21'}]
    tt_3 = [{'name': '波动异常2', 'xAxis': '2017-12'}, {'xAxis': '2017-22'}]
    tt.append(tt_1)
    tt.append(tt_2)
    tt.append(tt_3)
    return 0


def insert_met_reader():
    mysql = MySQL(2)
    mysql.mysql_connect()

    # 新建抄表责任人表格；插入抄表责任人
    # sql_0 = 'SELECT sta_num,met_reader FROM source_sta_meter WHERE met_reader !='' GROUP BY sta_num'
    # result_0 = mysql.query(sql_0)
    # for i in range(len(result_0)):
    #     sql = """insert into basic_reader_list(sta_num, met_reader)VALUES('{1}', '{2}')""".format(result_0[i][0], result_0[i][1])
    #     print('====sql:==', sql)
    #     mysql.executesql(sql)
    #     mysql.commitdata()

    # 对低压的表做sta_no 提取
    sql_0 = 'select sta_no from xgdl_low_voltage_user GROUP BY sta_no'
    result_0 = mysql.query(sql_0)
    for i in range(len(result_0)):
        sql = """insert into xgdl_low_voltage_user_sta_no(sta_no)VALUES('{1}')""".format(result_0[i][0])
        print('====sql:==', sql)
        mysql.executesql(sql)
        mysql.commitdata()

    mysql.mysql_close()
    return 1



def insert_city():
    mysql = MySQL(2)
    mysql.mysql_connect()

    city_list =[]

    sta_list_all = []
    sql_0 = 'SELECT sta_num FROM basic_sta_list GROUP BY sta_num'
    result_0 = mysql.query(sql_0)
    for i in range(len(result_0)):
        sta_list_all.append(result_0[i][0])

    sta_list_1 = []
    sql_1 = 'SELECT sta_no,city FROM xgdl_high_voltage_user GROUP BY sta_no'
    result_1 = mysql.query(sql_1)
    for i in range(len(result_1)):
        sta_list_1.append(result_1[i][0])

    sta_list_2 = []
    sql_2 = 'SELECT sta_no,city FROM xgdl_low_voltage_user GROUP BY sta_no'
    result_2 = mysql.query(sql_2)
    for i in range(len(result_2)):
        sta_list_2.append(result_2[i][0])

    sta_list_3 = []
    sql_3 = 'SELECT sta_no,city FROM Xgdl_Basic_Stalist GROUP BY sta_no'
    result_3 = mysql.query(sql_3)
    for i in range(len(result_3)):
        sta_list_3.append(result_3[i][0])

    sta_list_4 = []
    sql_4 = 'SELECT sta_num,cou_city FROM source_sta_list GROUP BY sta_num'
    result_4 = mysql.query(sql_4)
    for i in range(len(result_4)):
        sta_list_4.append(result_4[i][0])

    sta_list_5 = []
    sql_5 = 'SELECT sta_num,area FROM source_ydcb_record GROUP BY sta_num'
    result_5 = mysql.query(sql_5)
    for i in range(len(result_5)):
        sta_list_5.append(result_5[i][0])

    for i in range(len(sta_list_all)):
        sigle = []
        if sta_list_all[i] in sta_list_1:
            sigle.append(sta_list_all[i])
            for j in range(len(sta_list_1)):
                if result_1[j][0] == sta_list_all[i]:
                    sigle.append(result_1[j][1])
                    break
        elif sta_list_all[i] in sta_list_2:
            sigle.append(sta_list_all[i])
            for j in range(len(sta_list_2)):
                if result_2[j][0] == sta_list_all[i]:
                    sigle.append(result_2[j][1])
                    break
        elif sta_list_all[i] in sta_list_3:
            sigle.append(sta_list_all[i])
            for j in range(len(sta_list_3)):
                if result_3[j][0] == sta_list_all[i]:
                    sigle.append(result_3[j][1])
                    break
        elif sta_list_all[i] in sta_list_4:
            sigle.append(sta_list_all[i])
            for j in range(len(sta_list_4)):
                if result_4[j][0] == sta_list_all[i]:
                    sigle.append(result_4[j][1])
                    break
        elif sta_list_all[i] in sta_list_5:
            sigle.append(sta_list_all[i])
            for j in range(len(sta_list_5)):
                if result_5[j][0] == sta_list_all[i]:
                    sigle.append(result_5[j][1])
                    break
        else:
            sigle.append(sta_list_all[i])
            sigle.append('')

        city_list.append(sigle)
    print('--city_list:--', city_list)
    for i in range(len(city_list)):
        sql = """insert into basic_city_list(sta_no, city)VALUES('{1}', '{2}')""".format(city_list[i][0], city_list[i][1])
        print('====sql:==', sql)
        mysql.executesql(sql)
        mysql.commitdata()

    mysql.mysql_close()
    return 1


if __name__ == '__main__':
    # token = get_authtoken()
    # print('token:', token)
    # a = insert_met_reader()
    a = insert_city()
