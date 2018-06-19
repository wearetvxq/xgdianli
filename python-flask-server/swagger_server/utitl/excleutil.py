# -*- coding: UTF-8 -*-
from swagger_server.utitl.mysqlset import MySQL
import xlrd
import math
import datetime

'''for i in range(49):
    print("'{"+str(i)+"}', ", end='')'''


class ExcleUtil:
    @staticmethod
    def readfiletodb(filepath):
        # 1. 判断是什么文件
        # 2. 分文件导入

        print('-sss-',filepath.split("/")[1].split(".")[0])

        if __name__ == "__main__":
            print("打开Excle")
        data = xlrd.open_workbook(filepath)
        all_count = []
        count = [0, 0]
        if filepath.split("/")[1].split(".")[0] == "可开发容量监测营销数据":
            all_c = []
            all_c.append(filepath.split("/")[1].split(".")[0])
            table = data.sheets()[0]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if row[11] != '':
                                row[11] = str(xlrd.xldate.xldate_as_datetime(row[11], 0))
                            sql = """insert into zsdl_expansion(empty1, unit_code, power_unit, worksheet_states, apply_number, user_number, electricity_address, business_form, industry_form, supply_voltage, application_capacity, application_time, link_name, power_type, area_number, area_name, area_capacity, line_number, lines_name, substation_code, substation_name) VALUES ('{0}', {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}')""".format(row[0], row[1], row[2], row[3],row[4],row[5],row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13],row[14], row[15],row[16], row[17], row[18], row[19], row[20])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            all_c.append(count)
            all_count.append(all_c)
        elif filepath.split("/")[1].split(".")[0] == "可开发容量监测营销数据（销户）":
            all_c = []
            all_c.append(filepath.split("/")[1].split(".")[0])
            table = data.sheets()[0]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)

                            if row[11] != '':
                                row[11] = str(xlrd.xldate.xldate_as_datetime(row[11], 0))

                            sql = """insert into zsdl_closeaccount (unit_code, power_unit, worksheet_states, apply_number, user_number, electricity_address, business_form, industry_form, supply_voltage, application_capacity, application_time, link_name, power_type, area_number, area_name, area_capacity, line_number, lines_name, substation_code, substation_name) VALUES ('{0}','{1}', '{2}','{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}')""".format(row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19],row[20])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
                    all_count.append(all_c)
        elif filepath.split("/")[1].split(".")[0] == "附件：配网运行效率“大数据”挖掘分析数据需求表（浙江反馈表1-7）":
            all_c = []
            all_c.append(filepath.split("/")[1].split(".")[0])
            # -------------------经济使用情况------2-------------------------
            table = data.sheets()[2]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 3
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)

                            sql = """insert into zsdl_setupnet_econnmy (prefecture_cityname, area_name, area_land, GDP, GDP_upspeed, three_proportion, population_endyear, pre_gdp, urbanization_rate, total_amount) VALUES ('{0}','{1}', '{2}','{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')""".format(row[0],row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                            print('--sql-10-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            # -------------------经济使用情况 完---------2----------------------
            # -------------------供电可靠性 开始--4-----------------------------
            table = data.sheets()[4]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 4
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)

                            sql = """insert into zsdl_setupnet_reliability (companyname_city, companyname_area, statistics_type, power_reliability, power_cut_time, power_cut_times, number_of_blackouts, starved_feed_electric) VALUES ('{0}','{1}', '{2}','{3}', '{4}', '{5}', '{6}', '{7}')""".format(
                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            # -------------------供电可靠性 结束------4-------------------------

            # -------------------电量负荷 开始------3-------------------------
            table = data.sheets()[3]
            print('--table---', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 4
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if row[1] == '全省':
                                print('---全省--')
                            else:
                                print('--非-')

                            sql = """insert into zsdl_setupnet_powerload (companyname_city, companyname_area, total_electricallod, total_wattage, tertiaryandinmate_wattage, industry_2, industry_3, inmate, pre_wattage,pre_life_wattage, below110_original_value, NULL4, add_money) VALUES ('{0}','{1}', '{2}','{3}', '{4}', '{5}', '{6}', '{7}','{8}','{9}', '{10}','{11}', '{12}')""".format(
                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
                            print('--sql-10-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            # -------------------电量负荷 结束--------3-----------------------

            # -------------------配网区域 开始----------5-------------------------
            table = data.sheets()[5]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 3
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if type(row[0]) == float:
                                sql = """insert into zsdl_setupnet_netarea (order_number, companyname_provincial, companyname_city, companyname_area, area_name, service_area_type, zone_boundary_describe, area_of_region,regional_function_type, area_maximum_load, synthetic_voltage_yield,electric_reliability, below110_lineloss_rate, below10_lineloss_rate) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}')""".format(
                                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                    row[11], row[12], row[13])
                                if __name__ == "__main__":
                                    print("处理：" + row[0])
                                try:
                                    result = mysql.executesql(sql)
                                except Exception:
                                    print('-失败---', sql)
                                    m += 1
                                    pass
                                j = i
                            else:
                                nrows = nrows - 1
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    print('--successCount--', successCount)
                    count = [nrows - 1, successCount - m]
                    print('--count--', count)
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            print('--all_count--', all_count)
            # -------------------配网区域 结束--------5-----------------------

            # -------------------高压 开始----------6-------------------------
            table = data.sheets()[6]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 3
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if row[14] != '':
                                row[14] = str(xlrd.xldate.xldate_as_datetime(row[14], 0))

                            # 'id', 'order_number', 'companyname_provincial', 'companyname_city', 'companyname_area', 'area_name', 'service_area_type', 'valtage_classes', 'substation_name', 'transformer_name', 'dispatch_id', 'pms_id', 'rated_capacity', 'put_the_date', 'city_country_network', 'regionalism', 'manufacture_factory', 'no_load_loss', 'assets_properties', 'running_status', 'winding_type', 'installation_site', 'value_of_qquipment', 'load_diagram']

                            sql = """insert into zsdl_setupnet_highvoltage (order_number, companyname_provincial, companyname_city, companyname_area, area_name, service_area_type, valtage_classes, line_name, dispatch_id, pms_id,devices_type, setup_way, total_track_length, max_allowable_current, put_the_date,city_country_network, regionalism, manufacture_factory, assets_properties,running_status, typeof_guid_structure, value_of_qquipment, max_current,load_diagram) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}')""".format(row[0], row[1], row[2], row[3],row[4],row[5],row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13],str(row[14]), str(row[15]),row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            # -------------------高压 结束--------6-----------------------

            # -------------------主变 开始----------7-------------------------
            table = data.sheets()[7]
            print('--table---', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 3
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if row[12] != '':
                                row[12] = str(xlrd.xldate.xldate_as_datetime(row[12], 0))

                            sql = """insert into zsdl_setupnet_mainchange (order_number, companyname_provincial, companyname_city, companyname_area, area_name, service_area_type, valtage_classes, substation_name, transformer_name, dispatch_id, pms_id, rated_capacity, put_the_date, city_country_network, regionalism, manufacture_factory, no_load_loss, assets_properties, running_status, winding_type, installation_site, value_of_qquipment, load_diagram) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}')""".format(
                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12], row[13], row[14], row[15], str(row[16]), row[17], row[18],
                                row[19], row[20], row[21], row[22])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)
            # -------------------主变 结束--------7-----------------------

            # -------------------中压 开始----------8-------------------------
            table = data.sheets()[8]
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        if p == 1:
                            start = 3
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            row = table.row_values(i)
                            if row[14] != '':
                                row[14] = str(xlrd.xldate.xldate_as_datetime(row[14], 0))


                            sql = """insert into zsdl_setupnet_middlevoltage (order_number, companyname_provincial, companyname_city, companyname_area, area_name, service_area_type, valtage_classes, line_name, dispatch_id,  pms_id, line_type, line_category, total_track_length, max_allowable_current, put_the_date, city_country_network, regionalism, manufacture_factory, assets_properties, running_status, start_power_station, typeof_guid_structure, value_of_qquipment, max_current, load_diagram) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}','{23}', '{24}')""".format(
                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12], row[13], row[14], row[15], str(row[16]), row[17], row[18],
                                row[19], row[20], row[21], row[22], row[23], row[24])
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                result = mysql.executesql(sql)
                            except Exception:
                                print('-失败---', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
                    all_c.append(count)

            # -------------------中压 结束--------8-----------------------
            all_count.append(all_c)
        else:
            print('--filepath-err!-')
        return all_count


class ExcleUtil1:
    @staticmethod
    def readfiletodb(arg, filepath):
        # 1. 判断是什么文件
        # 2. 分文件导入
        print('--comming-1-')
        if __name__ == "__main__":
            print("打开Excle")
        data = xlrd.open_workbook(filepath)
        if arg =='设备数据':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    print('--0--')
                    mysql.mysql_connect()
                    print('--1--')
                    try:
                        print('comming1')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            row = table.row_values(i)
                            print('---row: ', row)
                            print('==========================================')
                            sql = "insert into piliang_import (city, sta_name, sta_num, type, pow, produce, sb_type) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                            print('--sql-sb_import-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('sb_import')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err sb_import:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                         print('上传error')
                         pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')

        if arg == '低压':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    print('--0--')
                    mysql.mysql_connect()
                    print('--1--')
                    try:
                        print('comming1')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            row = table.row_values(i)
                            print('---row: ', row)

                            if row[9] != '':
                                row[9] = str(xlrd.xldate.xldate_as_datetime(row[9], 0)).split(' ')[0]

                            print('--row[9]--', row[9])
                            sql = """
                               insert into xgdl_low_voltage_user
                               (city, sta_no, sta_name, user_no, sta_type, layout, user_name, ele_unit, met_address, `date`, active_ele, total_ratio)
                               VALUES
                               ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')
                               """.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                          row[7], row[8], row[9], row[10], row[11])
                            print('--sql-低压-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('低压')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err 低压:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')
        elif arg == '高压':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    print('--0--')
                    mysql.mysql_connect()
                    print('--1--')
                    try:
                        print('comming1')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        # 数据导入1
                        for i in range(start, endindex):
                            print('i:', i)
                            row = list(table.row_values(i))
                            print('---row_1: ', row)
                            print('---row_1: ', row[8])
                            if row[9] != '':
                                print('row[8]')
                                row[8] = str(xlrd.xldate.xldate_as_datetime(row[8], 0)).split(' ')[0]

                            print('--row[8]--', row[8])
                            sql = """
                               insert into xgdl_high_voltage_user
                               (city, sta_no, sta_name, user_no, sta_type, layout, user_name, ele_unit, `date`, 3_active_ele, 3_not_active_ele,total_ratio, ele_curve)
                               VALUES
                               ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}','{12}')
                               """.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],row[12])
                            print('--sql-00-', sql)

                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('try')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err:', sql)
                                m += 1
                                pass
                            j = i
                        # 测点数据导入
                        for i in range(start, endindex):
                            print('i:', i)
                            row = table.row_values(i)
                            print('---row: ', row)

                            if row[8] != '':
                                row[8] = str(xlrd.xldate.xldate_as_datetime(row[8], 0)).split(' ')[0]

                            print('--row[8]--', row[8])

                            for z in range(96):
                                print('--i:--', i)
                                if row[13 + z] != '' and row[13 + z] != 0 and row[13 + z] != '0':
                                    if str(row[13 + z])[:1] == '.':
                                        row_13_z = '0' + str(row[13 + z])
                                    else:
                                        row_13_z = str(row[13 + z])
                                    flag = 15 * (z + 1)
                                    print('---flag:-', flag)
                                    t_time = (
                                    datetime.datetime.strptime('00:00:00', "%H:%M:%S") + datetime.timedelta(
                                        minutes=flag)).strftime("%H:%M:%S")
                                    sql = """insert into xgdl_test_point(sta_no, sta_name, `date`, ele_curve, `value`)VALUES('{0}', '{1}', '{2}', '{3}', '{4}')""" \
                                        .format(row[1], row[2],
                                                str(datetime.datetime.strptime(row[8], "%Y-%m-%d")).split(' ')[
                                                    0] + ' ' + str(t_time), row[12], row_13_z)
                                    print('====sql:==', sql)
                                    if __name__ == "__main__":
                                        print("处理：" + row[0])
                                    try:
                                        print('executesql')
                                        mysql.commitdata()
                                        result = mysql.executesql(sql)
                                        # mysql.executesql(sql)
                                        print('result: ', result)
                                    except Exception:
                                        print('err:', sql)
                                        m += 1
                                        pass
                            # j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------')
        elif arg == '基站电表信息':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    print('--0--')
                    mysql.mysql_connect()
                    print('--1--')
                    try:
                        print('comming1')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            row = table.row_values(i)
                            print('---row: ', row)
                            print('---row[9]: ', row[9])

                            # if row[9] != '':
                            #     print('---row[9]: ', row[9])
                            #     a = xlrd.xldate.xldate_as_datetime(row[9], 0)
                            #     print('----a: ', a)
                            #     print('---row[9]00: ', xlrd.xldate.xldate_as_datetime(row[9], 0))
                            #     row[9] = str(xlrd.xldate.xldate_as_datetime(row[9], 0)).split(' ')[0]

                            print('--row[9]-1-', row[9])
                            sql = """insert into source_sta_meter(sta_num, stat_name, met_num, met_reader, met_reader_ph, met_type, max_code_value, magni, load_time, natu_unit, met_status, sta_type, distribut)VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}','{12}')""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[9], row[11], row[12], row[13], row[14])
                            print('--sql-低压-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('低压')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err 低压:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')
        elif arg == '基站机房的用电相关资料':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    print('--0--')
                    mysql.mysql_connect()
                    print('--1--')
                    try:
                        print('comming1基站机房的用电相关资料')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            row = table.row_values(i)

                            sql = """insert into source_sta_elec(area, site_code, tower_name, yd_name, yd_current, lt_current, dx_current)VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                            print('--sql-低压-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('低压')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err 低压:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')
        elif arg == '基站清单':
            table = data.sheets()[1]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        print('comming1基站清单')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            print('row2: ', table.row_values(2))
                            row = table.row_values(i)
                            print('--row: ', row)
                            sql = """insert into source_sta_list(behalf_of_comp, cou_city, sta_name1, sta_deta, acco_type, move_tower, crossed, `month`, high_sites, sta_num, sta_name, degree, elec_bill)VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')""".format(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13])
                            print('--sql-基站清单-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('基站清单')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err 低压:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')
        elif arg == '抄表记录':
            table = data.sheets()[0]
            print('--data-:-', data)
            print('--table-:-', table)
            if __name__ == "__main__":
                print("打开完毕！")
            nrows = table.nrows
            print('--nrows-:-', nrows)
            # ncols = table.ncols
            if nrows >= 1:
                successCount = 0
                j = 0
                m = 0
                # ---------每1000条进行一次数据导入--------------
                rowCount = nrows  # 导入总数
                print('--rowCount-:-', rowCount)
                pageCount = 0  # 页数
                if rowCount % 1000 == 0:
                    pageCount = int(rowCount / 1000)
                else:
                    # 向下取整
                    pageCount = int(math.floor(rowCount / 1000) + 1)
                print('--pageCount-:-', pageCount)
                mysql = MySQL(2)
                for p in range(1, pageCount + 1):
                    print('--p-:-', p)
                    if nrows < 1000:
                        endindex = nrows
                    else:
                        if nrows >= p * 1000:
                            endindex = p * 1000
                        else:
                            endindex = nrows
                    mysql.mysql_connect()
                    try:
                        print('comming1抄表记录')
                        if p == 1:
                            start = 1
                        else:
                            start = p * 1000 - 1000
                        for i in range(start, endindex):
                            print('i:', i)
                            print('row2: ', table.row_values(2))
                            row = table.row_values(i)
                            print('--row: ', row)
                            sql = """insert into source_ydcb_record(area, sta_num, sta_name, sta_type, sta_distr, met_num, start, stop, power_cons, price, bill, last_read_time, read_time, imp_time, reim_status, transcoded, met_days, daily_cons, chan_stop, site_attr)VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}')""".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[16], row[17], row[19], row[20], row[21], row[23])
                            print('--sql-抄表记录-', sql)
                            if __name__ == "__main__":
                                print("处理：" + row[0])
                            try:
                                print('基站清单')
                                mysql.commitdata()
                                result = mysql.executesql(sql)
                                # mysql.executesql(sql)
                                print('result: ', result)
                            except Exception:
                                print('err 低压:', sql)
                                m += 1
                                pass
                            j = i
                    except Exception:
                        print('上传error')
                        pass
                    finally:
                        if i > j:
                            successCount = j
                        else:
                            successCount = i
                    count = [nrows - 1, successCount - m]
                    mysql.commitdata()
                    mysql.mysql_close()
            print('--------------------------')
        elif arg == '客户用电信息':
            table_tst = data.sheets()
            print('---table_test--: ', table_tst)
            print('---table_test--: ', len(table_tst))
            for i in range(len(table_tst)):
                print('-----iiiii:', i)
                if data.sheets()[i].row_values(0)[0] == '用户编号':
                    table = data.sheets()[i]
                    if __name__ == "__main__":
                        print("打开完毕！")
                    nrows = table.nrows
                    print('--nrows-:-', nrows)
                    # ncols = table.ncols
                    if nrows >= 1:
                        successCount = 0
                        j = 0
                        m = 0
                        # ---------每1000条进行一次数据导入--------------
                        rowCount = nrows  # 导入总数
                        print('--rowCount-:-', rowCount)
                        pageCount = 0  # 页数
                        if rowCount % 1000 == 0:
                            pageCount = int(rowCount / 1000)
                        else:
                            # 向下取整
                            pageCount = int(math.floor(rowCount / 1000) + 1)
                        print('--pageCount-:-', pageCount)
                        mysql = MySQL(2)
                        for p in range(1, pageCount + 1):
                            print('--p-:-', p)
                            if nrows < 1000:
                                endindex = nrows
                            else:
                                if nrows >= p * 1000:
                                    endindex = p * 1000
                                else:
                                    endindex = nrows
                            mysql.mysql_connect()
                            try:
                                print('comming1客户用电信息')
                                if p == 1:
                                    start = 1
                                else:
                                    start = p * 1000 - 1000
                                for i in range(start, endindex):
                                    print('i:', i)
                                    print('row2: ', table.row_values(2))
                                    row = table.row_values(i)
                                    print('--row: ', row)
                                    if row[0] != '' and row[1] != '':
                                        sql = """insert into source_elec_info(user_id, user_name, met_num, `date`, total_num, peak_num, flat_num, valley_num, total_power, peak_power, flat_charge, valley_elec, freeze_time, storage_time, point_num, mail_addr, addr_code, area_code, termi_name, met_chip_manu, term_chip_manu, copy_table_num, met_reader, copy_day, elec_addr, elec_cate, power_unit, supe_unit)VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}', '{24}', '{25}', '{26}', '{27}')""".format(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[10],
                                            row[11], row[12], row[13], row[16], row[17], row[18], row[19], row[20],
                                            row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28],
                                            row[29], row[30], row[31])
                                        print('--sql-客户用电信息-', sql)
                                        if __name__ == "__main__":
                                            print("处理：" + row[0])
                                        try:
                                            print('基站清单')
                                            mysql.commitdata()
                                            result = mysql.executesql(sql)
                                            # mysql.executesql(sql)
                                            print('result: ', result)
                                        except Exception:
                                            print('err 低压:', sql)
                                            m += 1
                                            pass
                                    j = i
                            except Exception:
                                print('上传error')
                                pass
                            finally:
                                if i > j:
                                    successCount = j
                                else:
                                    successCount = i
                            count = [nrows - 1, successCount - m]
                            mysql.commitdata()
                            mysql.mysql_close()
                    print('--------------------------')
                else:
                    pass

        return count

    @staticmethod
    def updatetype():
        mysql = MySQL(2)
        mysql.mysql_connect()
        mysql.executesql("truncate table problemtype")
        sql = "select DISTINCT(problemtype) from warnorderinfo"
        result = mysql.query(sql)
        for i in range(len(result)):
            typestr = result[i][0]
            typearray = typestr.split('-')
            if (len(typearray) < 3):
                typearray.append("null")
            else:
                typesql = " insert into  problemtype (type1,type2,type3) values('{0}','{1}','{2}')".format(typearray[0], typearray[1], typearray[2])
            try:
                mysql.executesql(typesql)
            except Exception:
                print(sql)
                pass
        mysql.commitdata()
        mysql.mysql_close()

    @staticmethod
    def updatecityinfo():
        mysql = MySQL(2)
        mysql.mysql_connect()
        mysql.executesql("truncate table cityinfo")
        sql = "SELECT distinct executecity,executearea FROM warnorderinfo where executearea !='' order by executecity"
        result = mysql.query(sql)
        for i in range(len(result)):
            if(len(result[i][0])>10):
                continue
            typesql = " insert into  cityinfo (cityname,areaname) values('{}','{}')".format(result[i][0], result[i][1])
            try:
                mysql.executesql(typesql)
            except Exception:
                pass
        mysql.commitdata()
        mysql.mysql_close()


def main():
    # ExcleUtil.readfiletodb("F:\\采集\\20160725-20160825故障工单（含性能）.xlsx")
    # ExcleUtil.refrusetype()
    ExcleUtil.updatecityinfo()
    pass


if __name__ == "__main__":
     main()
