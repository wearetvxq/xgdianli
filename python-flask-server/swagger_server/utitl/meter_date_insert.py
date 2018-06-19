# -*- coding: UTF-8 -*-
import connexion
from datetime import date
from typing import List, Dict
from six import iteritems
from flask import json, jsonify
from flask import Response
import datetime
import calendar
import math
# import jwt.jwa
# from jwt import jwa
import itsdangerous
import time
import re
import xlrd

from .Jwts import jwt_s
from .common import com
from .mysqlset import MySQL
import multiprocessing



# ##############################################
#                                              #
#                  电表数据导入                #
#                                              #
# ##############################################


# 电表数据导入
class meter_data:
    def commit_date_single(self,meter_name='',table_name=''):
        flag = 0
        try:
            jwt_s.getGroupMeter()
            result_list = jwt_s.getRealTime(meter_name)

            print('result_list: ', result_list)
            result_list_1 = eval(result_list)
            payload = result_list_1['payload']
            payload_new_1 = eval(str(payload))
            if 'factor' in payload_new_1:
                temperature = payload['temperature']
                type = payload['type']
                voltage = payload['voltage']
                kWh = payload['kWh']
                kW = payload['kW']
                kVar = payload['kVar']
                state = payload['state']
                # timestamp = payload['timestamp']
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                current = payload['current']
                factor = payload['factor']
                devId = payload['devId']
            else:
                temperature = ''
                type = ''
                voltage = ''
                kWh = ''
                kW = ''
                kVar = ''
                state = ''
                # timestamp = payload['timestamp']
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                current = ''
                factor = ''
                devId = ''

            # print('temperature: ', temperature)
            # print('type: ', type)
            # print('voltage: ', voltage)
            # print('kWh: ', kWh)
            # print('kW: ', kW)
            # print('kVar: ', kVar)
            # print('state: ', state)
            # print('timestamp: ', timestamp)
            # print('current: ', current)
            # print('factor: ', factor)
            # print('devId: ', devId)
            # _________________
            title = ['型号', '电压', '用电量(kWh)', '有功功率(kW)', '无功功率(kVar)', '时间点', '电流', '功率因素', '设备ID']
            mysql = MySQL(2)
            mysql.mysql_connect()
            sql = """insert into {0}(temperature, `type`, voltage, kWh, `kW`,kVar,`timestamp`,`current`,factor,devId)VALUES('{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}', '{8}', '{9}','{10}')""".format(
                table_name, temperature, type, voltage, kWh, kW, kVar, timestamp, current, factor, devId)

            print('====sql:==', sql)

            mysql.executesql(sql)
            mysql.commitdata()
            flag = 1
        except:
            flag = 0
            print('数据导入错误：', meter_name)
            time.sleep(60)

        return flag

    def get_real_time_data(self):
        meter_list = ['161211000010', '170311000004']
        table = ['xgdl_meter_161211000010', 'xgdl_meter_170311000004']
        while 1:
            for i in range(len(meter_list)):
                self.commit_date_single(meter_list[i], table[i])
            time.sleep(60)
        return 'ok'


    def insert_data(self):
        p = multiprocessing.Process(target=self.get_real_time_data)
        # 加上daemon属性
        p.daemon = True
        p.start()
        p.join()  # 设置daemon执行完结束的方法
        print("End!!")

meter = meter_data()