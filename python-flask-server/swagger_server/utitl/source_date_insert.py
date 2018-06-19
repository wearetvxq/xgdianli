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
from .excleutil import ExcleUtil1
import os


# ##############################################
#                                              #
#                  原始数据导入                #
#                                              #
# ##############################################


# 电表数据导入
class source_data:
    def data_extract(self,table=''):
        '''
        作用：新建表格，做数据提取
            1. 新建抄表责任人表格；插入抄表责任人
            2. 对低压的表做sta_no 提取
            3. 对高压的表做sta_no 提取
        :return:
        '''
        mysql = MySQL(2)
        mysql.mysql_connect()

        if table == '低压':
            # 首先清空表格
            sql = 'truncate table xgdl_low_valtage_user_sta_no_copy;'
            result = mysql.query(sql)
            print('result: ', result)
            # 对低压的表做sta_no 提取
            sql_0 = 'select sta_no,city from xgdl_low_voltage_user GROUP BY sta_no,city'
            result_0 = mysql.query(sql_0)
            print('----result_0--', result_0)
            for i in range(len(result_0)):
                sql = """insert into xgdl_low_valtage_user_sta_no_copy(sta_no,city)VALUES('{0}','{1}')""".format(result_0[i][0], result_0[i][1])
                print('====sql:==', sql)
                mysql.executesql(sql)
                mysql.commitdata()
        elif table == '高压':
            # 首先清空表格
            sql = 'truncate table xgdl_high_voltage_user_sta_no_copy;'
            result = mysql.query(sql)
            print('result: ', result)
            # 对高压的表做sta_no 提取
            sql_0 = 'select sta_no,city from xgdl_high_voltage_user GROUP BY sta_no,city'
            result_0 = mysql.query(sql_0)
            print('----result_0--', result_0)
            for i in range(len(result_0)):
                sql = """insert into xgdl_high_voltage_user_sta_no_copy(sta_no,city)VALUES('{0}','{1}')""".format(result_0[i][0], result_0[i][1])
                print('====sql:==', sql)
                mysql.executesql(sql)
                mysql.commitdata()

        mysql.mysql_close()
        return 1

    def scan_file(self):
        print('scan_file')
        base_abpath = os.path.abspath('./upload/')
        print(base_abpath)
        abpath_1 = "/".join([base_abpath, 'voltage_high'])  # 孝感移动高压
        abpath_2 = "/".join([base_abpath, 'voltage_low'])   # 孝感移动低压
        abpath_3 = "/".join([base_abpath, 'electric_info'])  # 基站电表信息
        abpath_4 = "/".join([base_abpath, 'computer_relate'])  # 基站机房的用电相关资料
        abpath_5 = "/".join([base_abpath, 'station_list'])   # 基站清单
        abpath_6 = "/".join([base_abpath, 'meter_reading'])  # 抄表记录
        abpath_7 = "/".join([base_abpath, 'user_ele_info'])  # 客户用电信息

        # 从不同的目录读取文件
        for f in os.listdir(abpath_1):
            destination = "/".join([abpath_1, f])
            print('destination_1:', destination)
            # 读取文件,导入数据
            ExcleUtil1.readfiletodb('孝感移动高压', destination)
            # 重写文件
            self.data_extract('高压')
            os.remove(destination)

        for f in os.listdir(abpath_2):
            destination = "/".join([abpath_2, f])
            print('destination_2:', destination)
            ExcleUtil1.readfiletodb('孝感移动低压', destination)
            # 重写文件
            self.data_extract('低压')
            os.remove(destination)

        for f in os.listdir(abpath_3):
            destination = "/".join([abpath_3, f])
            print('destination_3:', destination)
            ExcleUtil1.readfiletodb('基站电表信息', destination)
            os.remove(destination)

        for f in os.listdir(abpath_4):
            destination = "/".join([abpath_4, f])
            print('destination_4:', destination)
            ExcleUtil1.readfiletodb('基站机房的用电相关资料', destination)
            os.remove(destination)

        for f in os.listdir(abpath_5):
            destination = "/".join([abpath_5, f])
            print('destination_5:', destination)
            ExcleUtil1.readfiletodb('基站清单', destination)
            os.remove(destination)

        for f in os.listdir(abpath_6):
            destination = "/".join([abpath_6, f])
            print('destination_6:', destination)
            ExcleUtil1.readfiletodb('抄表记录', destination)
            os.remove(destination)

        for f in os.listdir(abpath_7):
            destination = "/".join([abpath_7, f])
            print('destination_7:', destination)
            ExcleUtil1.readfiletodb('客户用电信息', destination)
            os.remove(destination)

        return 1

    def all_file_insert(self):
        '''
        1.每隔半小时获取一次时间，当时间到了1点的时候，开始扫描文件，写入文件，入库文件完成后，直接删除文件。
        :return:
        '''
        while 1:
            # 获取当前时间
            timestamp = str(time.strftime('%H', time.localtime(time.time())))
            time.sleep(1800)
            if timestamp == '23':
                print('开始扫描')
                self.scan_file()

        return 'ok'

    def source_insert_data(self):
        p = multiprocessing.Process(target=self.all_file_insert)
        # 加上daemon属性
        p.daemon = True
        p.start()
        p.join()  # 设置daemon执行完结束的方法
        print("End!!")

source = source_data()