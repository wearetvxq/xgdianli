# -*- coding: UTF-8 -*-
import connexion
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
from swagger_server.utitl.mysqlset import MySQL
from flask import json, jsonify
from flask import Response,request
from swagger_server.utitl.excleutil import ExcleUtil1
import os, sys
import time
import math
import socket
import random
import tarfile
import zipfile
import datetime
import os
from multiprocessing import Process, Queue, Array, RLock
import multiprocessing


# ##############################################
#                                              #
#                  录入页面                    #
#                                              #
# ##############################################

# 1.导入的文件类型
def import_file_type():
    resultdict = {}
    resultdict['import_file_type'] = ['设备数据']


    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = round(bytes / 1024, 2)
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = round(kb / 1024, 2)
        if M >= 1024:
            G = round(M / 1024, 2)
            return "%sG" % (G)
        else:
            return "%sM" % (M)
    else:
        return "%sKB" % (kb)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 第二版
# 数据导入
# def FileImport_old(arg='', description=''):
#     '''
#         创建进程完成对数据的表的直接读取
#     '''
#     print('--:', request.method)
#     p = multiprocessing.Process(target=data_import, args=(arg, description, request.method))
#     # 加上daemon属性
#     p.daemon = True
#     p.start()
#     p.join()  # 设置daemon执行完结束的方法
#     print("End!!")


def FileImport(arg='', description=''):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    if request.method == 'POST':
        abpath = os.path.abspath('./upload/') + '/'

        f = request.files["file"]
        random_string = str(random.randint(100000000, 10000000000))

        file_name_path = ''
        if arg == '高压':
            file_name_path = abpath + 'voltage_high/' + random_string + '_voltage_high.xls'
            f.save(abpath + 'voltage_high/' + random_string + '_voltage_high.xls')
        elif arg =='设备数据':
            print (abpath,random_string)
            file_name_path=abpath + 'sb_list/'+random_string + '_moban.xls'
            f.save(abpath + 'sb_list/' + random_string + '_moban.xls')
        elif arg == '低压':
            file_name_path = abpath + 'voltage_low/' + random_string + '_voltage_low.xlsx'
            f.save(abpath + 'voltage_low/' + random_string + '_voltage_low.xlsx')
        elif arg == '基站清单':
            file_name_path = abpath + 'station_list/' + random_string + '_station_list.xls'
            f.save(abpath + 'station_list/' + random_string + '_station_list.xls')
        elif arg == '抄表记录':
            file_name_path = abpath + 'meter_reading/' + random_string + '_meter_reading.xls'
            f.save(abpath + 'meter_reading/' + random_string + '_meter_reading.xls')
        elif arg == '供电局缴费表号':
            file_name_path = abpath + 'pay_records/' + random_string + '_pay_records.xls'
            f.save(abpath + 'pay_records/' + random_string + '_pay_records.xls')
        elif arg == '基站电表信息':
            file_name_path = abpath + 'electric_info/' + random_string + '_electric_info.xls'
            f.save(abpath + 'electric_info/' + random_string + '_electric_info.xls')
        elif arg == '基站机房的用电相关资料':
            file_name_path = abpath + 'computer_relate/' + random_string + '_computer_relate.xls'
            f.save(abpath + 'computer_relate/' + random_string + '_computer_relate.xls')
        elif arg == '客户用电信息':
            file_name_path = abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls'
            f.save(abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls')
        else:
            print('-arg-err!--')

        # -------------------录入记录表格----------------
        # 名称、大小、时间、描述
        # 1. f、
        for upload in request.files.getlist("file"):
            filename = upload.filename
        # 2. 大小
        filesize = getDocSize(file_name_path)
        # 3.时间
        currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mysql = MySQL(2)
        mysql.mysql_connect()
        sql = " insert into xgdl_uploadfile_information (filename,filesize,description,uploadtime) value ('{}','{}','{}','{}') ".format(
            str(filename), filesize, description, currenttime)
        mysql.executesql(sql)

        mysql.commitdata()
        mysql.mysql_close()
        # 实时数据入库
        TicketImport(arg, file_name_path)
        # -------------------录入记录表格----------------
        reps = jsonify(1)
    else:
        reps = jsonify(-1)

    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 数据导入
def TicketImport(arg='', file_name_path=''):
    abpath = os.path.abspath(file_name_path)

    flag = 0
    try:
        destination = abpath
        all_count = ExcleUtil1.readfiletodb(arg, destination)
        flag = 1
    except:
        flag = 0
    print (flag)
    reps = jsonify(flag)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 第一版
# 2. 导入前端文件到本地
def FileImport_old(arg='', description=''):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    if request.method == 'POST':
        abpath = os.path.abspath('./upload/') + '/'

        f = request.files["file"]
        random_string = str(random.randint(100000000, 10000000000))

        file_name_path = ''
        if arg == '高压':
            file_name_path = abpath + 'voltage_high/' + random_string + '_voltage_high.xls'
            f.save(abpath + 'voltage_high/' + random_string + '_voltage_high.xls')
        elif arg == '低压':
            file_name_path = abpath + 'voltage_low/' + random_string + '_voltage_low.xlsx'
            f.save(abpath + 'voltage_low/' + random_string + '_voltage_low.xlsx')
        elif arg == '基站清单':
            file_name_path = abpath + 'station_list/' + random_string + '_station_list.xls'
            f.save(abpath + 'station_list/' + random_string + '_station_list.xls')
        elif arg == '抄表记录':
            file_name_path = abpath + 'meter_reading/' + random_string + '_meter_reading.xls'
            f.save(abpath + 'meter_reading/' + random_string + '_meter_reading.xls')
        elif arg == '供电局缴费表号':
            file_name_path = abpath + 'pay_records/' + random_string + '_pay_records.xls'
            f.save(abpath + 'pay_records/' + random_string + '_pay_records.xls')
        elif arg == '基站电表信息':
            file_name_path = abpath + 'electric_info/' + random_string + '_electric_info.xls'
            f.save(abpath + 'electric_info/' + random_string + '_electric_info.xls')
        elif arg == '基站机房的用电相关资料':
            file_name_path = abpath + 'computer_relate/' + random_string + '_computer_relate.xls'
            f.save(abpath + 'computer_relate/' + random_string + '_computer_relate.xls')
        elif arg == '客户用电信息':
            file_name_path = abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls'
            f.save(abpath + 'user_ele_info/' + random_string + '_user_ele_info.xls')
        else:
            print('-arg-err!--')

        # -------------------录入记录表格----------------
        # 名称、大小、时间、描述
        # 1. f、
        for upload in request.files.getlist("file"):
            filename = upload.filename
        # 2. 大小
        filesize = getDocSize(file_name_path)
        # 3.时间
        currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mysql = MySQL(2)
        mysql.mysql_connect()
        sql = " insert into xgdl_uploadfile_information (filename,filesize,description,uploadtime) value ('{}','{}','{}','{}') ".format(
            str(filename), filesize, description, currenttime)
        mysql.executesql(sql)

        mysql.commitdata()
        mysql.mysql_close()
        # -------------------录入记录表格----------------
        reps = jsonify(1)
    else:
        reps = jsonify(-1)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 3.展示导入结果
def showimport(PageIndex=1):
    resultdict = {}
    show = []
    # 1.标题：
    title_name = ['id', '文件名', '文件大小', '文件描述', '时间']
    resultdict["title_name"] = title_name
    # 2.获取录入结果
    mysql = MySQL(2)
    mysql.mysql_connect()
    import_record = "select id,filename,filesize,description,uploadtime from xgdl_uploadfile_information where 1=1 "
    result = mysql.query(import_record)
    mysql.mysql_close()
    resultList = []
    for i in range(len(result)):
        resultList.append(list(result[i]))
    resultList.reverse()

    # ---------分页---------
    rowCount = len(resultList)
    pageCount = 0
    if rowCount % 10 == 0:
        pageCount = rowCount / 10
    else:
        # 向下取整
        pageCount = math.floor(rowCount / 10) + 1

    page_resultList = []
    if len(resultList) < 10:
        endindex = len(resultList)
    else:
        if len(resultList) >= PageIndex * 10:
            endindex = PageIndex * 10
        else:
            endindex = len(resultList)
    if resultList != []:
        for i in range((PageIndex * 10 - 10), endindex):
            page_resultList.append(resultList[i])
        resultdict["page_resultList"] = page_resultList
        resultdict["rowCount"] = rowCount
        resultdict["pageCount"] = pageCount
        # ------------------
    else:
        resultdict["page_resultList"] = []
        resultdict["rowCount"] = 0
        resultdict["pageCount"] = 0

    reps = jsonify(resultdict)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps
#下载接口
# def file_download(file_name=''):
#     mysql=MySQL(2)
#     mysql.mysql_connect()
#     if file_name!='':
#        sql="select filename filesize from xgdl_uploadfile_information WHERE filename='{}'".format(file_name)
#        print('----sql--:',sql)
#     result=mysql.query(sql)



# 4.删除接口：
def show_delete(file_id=0):
    mysql = MySQL(2)
    mysql.mysql_connect()
    import_record = "DELETE FROM xgdl_uploadfile_information WHERE id= {}".format(file_id)
    try:
        mysql.executesql(import_record)
        mysql.commitdata()
        mysql.mysql_close()
        reps = jsonify(1)
    except:
        reps = jsonify(-1)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


# 高压低压数据导入
# 1.录入
def TicketImport_old():
    abpath = os.path.abspath('./upload/high_low_date/')

    flag = 0
    try:
        # for f in os.listdir(abpath):
        destination = "/".join([abpath, 'high.xls'])
        all_count = ExcleUtil1.readfiletodb(destination)
        flag = 1
    except:
        flag = 0
    reps = jsonify(flag)
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps















# 5.分片测试
def file_split():
    if request.method == 'POST':
        f = request.files["file"]
        for upload in request.files.getlist("file"):
            filename = upload.filename.rsplit("/")[0]
            print(filename)
            f.save("C:/Users/flyminer/Desktop/split_test/" + filename)

    reps = jsonify("ok!")
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps



# 5.分片测试
def file_split_old1():
    name = request["name"]
    total = Convert.ToInt32(request["total"]);
    index = Convert.ToInt32(request["index"]);
    if request.method == 'POST':
        # f = request.files["file"]
        f = request.Files["data"]
        for upload in request.files.getlist("file"):
            filename = upload.filename.rsplit("/")[0]
            print(filename)
            f.save("C:/Users/flyminer/Desktop/split_test/" + filename)

    reps = jsonify("ok!")
    reps.headers["Access-Control-Allow-Origin"] = "*"
    return reps


"""
多进程分块读取文件
"""
WORKERS = 4
BLOCKSIZE = 100000000
FILE_SIZE = 0
def getFilesize(file):
  """
    获取要读取文件的大小
  """
  global FILE_SIZE
  fstream = open(file,'r')
  fstream.seek(0,os.SEEK_END)
  FILE_SIZE = fstream.tell()
  fstream.close()
def process_found(pid,array,file,rlock):
  global FILE_SIZE
  global JOB
  global PREFIX
  """
    进程处理
    Args:
      pid:进程编号
      array:进程间共享队列，用于标记各进程所读的文件块结束位置
      file:所读文件名称
    各个进程先从array中获取当前最大的值为起始位置startpossition
    结束的位置endpossition (startpossition+BLOCKSIZE) if (startpossition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
    if startpossition==FILE_SIZE则进程结束
    if startpossition==0则从0开始读取
    if startpossition!=0为防止行被block截断的情况，先读一行不处理，从下一行开始正式处理
    if 当前位置 <=endpossition 就readline
    否则越过边界，就从新查找array中的最大值
  """
  fstream = open(file,'r')
  while True:
    rlock.acquire()
    startpossition = max(array)
    endpossition = array[pid] = (startpossition+BLOCKSIZE) if (startpossition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
    rlock.release()
    if startpossition == FILE_SIZE:#end of the file
      break
    elif startpossition !=0:
      fstream.seek(startpossition)
      fstream.readline()
    pos = ss = fstream.tell()
    ostream = open('/data/download/tmp_pid'+str(pid)+'_jobs'+str(endpossition),'w')
    while pos<endpossition:
      #处理line
      line = fstream.readline()
      ostream.write(line)
      pos = fstream.tell()
    ostream.flush()
    ostream.close()
    ee = fstream.tell()
  fstream.close()
def main():
  global FILE_SIZE
  file = "/data/pds/download/scmcc_log/tmp_format_2011004.log"
  getFilesize(file)
  rlock = RLock()
  array = Array('l',WORKERS,lock=rlock)
  threads=[]
  for i in range(WORKERS):
    p=Process(target=process_found, args=[i,array,file,rlock])
    threads.append(p)
  for i in range(WORKERS):
    threads[i].start()
  for i in range(WORKERS):
    threads[i].join()
