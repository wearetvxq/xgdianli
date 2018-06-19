# - * - coding: utf-8 - * -
# from .mysqlset import MySQL
import json
import math
import datetime
from dateutil import rrule
import os

################################################
# 目录：
# 1. 测试
# 2. 分页
# 3.月份自动加1
# 4.月份自动减1
# 5.找出两个时间段，相差的月 数量
# 6.找到一段时间内的月列表
# 7.依据开始时间和天数获取时间的生成器
# 8.找到一段时间内天列表
# 9.删除指定目录下的所有文件
# 10.指定日期算出前n天或后n天日期
# 11.二维列表排序
# 12.两个日期相差的天数

################################################

class comm:
    def __init__(self):
        self.author = '张志勇'

    # 1. 测试
    def zzy_test(self, arg2=[]):
        print('---arg2:--', arg2)
        return (arg2)

    # 2. 分页
    def paging(self, resultList=[], everyPage_count=10, PageIndex=1):
        if len(resultList) != 0:
            rowCount = len(resultList)  # 总行数
            if rowCount % everyPage_count == 0:
                pageCount = rowCount / everyPage_count
            else:
                # 向下取整
                pageCount = math.floor(rowCount / everyPage_count) + 1

            page_resultList = []
            if len(resultList) < everyPage_count:
                endindex = len(resultList)
            else:
                if len(resultList) >= PageIndex * everyPage_count:
                    endindex = PageIndex * everyPage_count
                else:
                    endindex = len(resultList)
            if resultList != []:
                for i in range((PageIndex * everyPage_count - everyPage_count), endindex):
                    page_resultList.append(resultList[i])
        else:
            page_resultList = []
            rowCount = 0
            pageCount = 0
        return [page_resultList, rowCount, pageCount]

    # 3.月份自动加1
    # 参数格式：
        # dt: 2017-12
    def add_months(self, dt, months):
        print('---dt:-',dt)
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        return dt.replace(year=int(year), month=month)

    # 4.月份自动减1
    # 参数格式：# dt: 2017-12
    # 返回值：2017-11
    def minus_months(self, dt=''):
        print('-dt---')
        time_arr = dt.split('-')
        tyears = int(time_arr[0])
        tmonth = int(time_arr[1])-1
        if tmonth == 0:
            tmonth += 12
            tyears -= 1
        if tmonth < 10:
            tmonth = '0' + str(tmonth)
        print('-minus_months---', str(tyears) + '-' + str(tmonth))
        return str(tyears) + '-' + str(tmonth)

    # 5.找出两个时间段，相差的月 数量
    # 参数：StartDate、EndDate
    # 返回值：月数：2
    def get_months_count(self,StartDate,EndDate):
        months = rrule.rrule(rrule.MONTHLY, dtstart=StartDate, until=EndDate).count()
        print('-months-:', months)
        return months

    # 6.找到一段时间内的月列表：
    # 1.参数格式：
    #   时间：2010-12-12
    def get_month_list(self,StartDate='', EndDate=''):
        print('--StartDate----', StartDate)
        print('--EndDate----', EndDate)
        begin_date = str(StartDate)[:7]
        end_date = str(EndDate)[:7]
        date_list = []
        print('--begin_date----', begin_date)
        print('--end_date----', end_date)
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m")
        print('--begin_date----', begin_date)
        print('--end_date----', end_date)
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m")
            date_list.append(date_str)
            begin_date = self.add_months(begin_date, 1)
        print(date_list)
        return date_list

    # 7.依据开始时间和天数获取时间的生成器
    # 1.参数格式：
    #   时间：2010-12-12
    def gen_dates(self,b_date, days):
        day = datetime.timedelta(days=1)
        for i in range(days):
            yield b_date + day * i

    # 8.找到一段时间内天列表：
    # 1.参数格式：
    #   时间：2010-12-12
    def get_days_list(self,StartDate='', EndDate=''):
        dates = []
        start = datetime.datetime.strptime(StartDate, "%Y-%m-%d")
        end = datetime.datetime.strptime(EndDate, "%Y-%m-%d")
        for d in self.gen_dates(start, (end - start).days + 1):
            dates.append(str(d)[:10])
        return dates

    # 9.删除指定目录下的所有文件
    def delete_all_file(self,absolute_path=''):
        path_1 = os.path.abspath(absolute_path)
        path_0 = path_1.split('\\')
        path = ''
        for i in range(len(path_0)):
            path += path_0[i] + '/'
        try:
            for f in os.listdir(path):
                destination = "".join([path, f])
                os.remove(destination)
                # os.remove('E:/wamp/www/xgdl/download/456.xls')
                return 1
        except:
            return 0

    # 10.指定日期算出前n天或后n天日期
    # 参数：
    #     date：日期
    #     y_or_t：(1:以后；-1：往前)
    #     count:天数
    def get_y_t_date(self, date='', y_or_t='', count=1):
        if y_or_t == '1':
            day = datetime.datetime.strptime(str(date), "%Y-%m-%d") + datetime.timedelta(days=count)
        elif y_or_t == '-1':
            day = datetime.datetime.strptime(str(date), "%Y-%m-%d") - datetime.timedelta(days=count)
        return day

    # 11.二维列表排序
    def list_sort(self,result_list):
        result_list.sort(key=lambda x: x[1])
        result_list.reverse()
        return result_list

    # 12.两个日期相差的天数
    def days_apart(self,StartDate='', EndDate=''):
        start = datetime.datetime.strptime(StartDate, "%Y-%m-%d")
        end = datetime.datetime.strptime(EndDate, "%Y-%m-%d")
        days = (end - start).days
        print('--days--', days)
        return days


com = comm()

if __name__ == '__main__':
    print('comming class Common test!')
    # common = com()
    # common.get_month_list()
    # com.get_month_list()
    com.days_apart('2017-01-19', '2017-01-20')
