# -*- coding: UTF-8 -*-
import pymysql


# mysql操作类
class MySQL:
    type = ""
    conn = None

    def __init__(self, type):
        self.type = type

    # 链接库
    def mysql_connect(self):
        if self.type == 1:
            # self.conn = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='yuanshishuju_1')
            self.conn = pymysql.connect(host='192.168.1.112', port=3306, user='root', passwd='123456', db='xgdl', charset='utf8')
        elif self.type == 2:
            self.conn = pymysql.connect(host='39.108.165.149', port=3306, user='root', passwd='lcj123456', db='xgyd', charset='utf8')
            # self.conn = pymysql.connect(host='192.168.1.124', port=3306, user='root', passwd='123456', db='zhoushan_electric1', charset='utf8')
            # self.conn = pymysql.connect(host='192.168.1.124', port=3306, user='root', passwd='123456', db='zhoushan_fenbiao', charset='utf8')
            # self.conn = pymysql.connect(host='192.168.1.112', port=3306, user='root', passwd='123456', db='ngdl', charset='utf8')
        return self.conn

    # 关闭数据库
    def mysql_close(self):
        self.conn.close()

    # 查询
    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    #插入数据
    def Insert(self,sql):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor.fetchall()
    #更新数据库
    def Update(self,sql):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor.fetchall()
    #删除信息
    def Remove(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor.fetchall()

    # executeSql
    def executesql(self, sql):
        cursor = self.conn.cursor()
        re = cursor.execute(sql)
        return re

    def commitdata(self):
        self.conn.commit()

    def rollbackdata(self):
        self.conn.rollback()

    # insert
    def insert(self, tablename, dataarr):
        cursor = self.conn.cursor()
        sql = self.dealinsertdata(tablename, dataarr)
        re = cursor.execute(sql)
        self.conn.commit()
        return re

    # update
    def update(self, tablename, dataarr, where):
        cursor = self.conn.cursor()
        sql = self.dealupdatedata(tablename, dataarr, where)
        re = cursor.execute(sql)
        self.conn.commit()
        return re

    # delete
    def delete(self, tablename, where):
        cursor = self.conn.cursor()
        sql = "delete from " + tablename + " where " + where
        re = cursor.execute(sql)
        self.conn.commit()
        return re

    def insert_id(self):
        return self.conn.insert_id()

    def affected_rows(self):
        cursor = self.conn.cursor()
        return cursor.rowcount

    def dealinsertdata(self, tablename, data):
        key = []
        val = []
        for d, x in data.items():
            key.append("`" + d + "`")
            k = data.keys()
            val.append("'" + x + "'")

        field = ",".join(key)
        vals = ",".join(val)
        sql = "insert into " + tablename + "(" + field + ") values(" + vals + ")"
        return sql

    def dealupdatedata(self, tablename, data, condition):
        val = []
        updatestr = ""
        for d, x in data.items():
            val.append("`" + d + "` = " + "'" + x + "'")
        vals = ",".join(val)
        sql = "update " + tablename + " set " + vals + " where " + condition
        return sql

    # --------zzy new----------
    def excle_scroll(self):
        cursor = self.conn.cursor()
        cursor.scroll(0, mode='absolute')
        return 1

    def excle_fetchall(self):
        cursor = self.conn.cursor()
        return cursor.fetchall()

    def excle_description(self):
        cursor = self.conn.cursor()
        return cursor.description()

    # ------------------