# -*- coding: utf-8 -*-

#   基础模块
import time
import warnings
import os
import sys
import json

#   mysql相关
import pymysql



warnings.filterwarnings("ignore")


class MysqlSyn(object):
    def __init__(self):
        self.max_lines = 0        #   单张表迁移数据最大条目
        self.page_size = 2000       #   全数据量迁移时每页大小
        self.from_conn = None
        self.to_conn = None
        self.from_db = None
        self.to_db = None
        self.loadConf();

    #   配置文件读取
    def loadConf(self):
        path = os.path.join(os.path.abspath('.'), 'config.json')
        with open(path, encoding='utf-8') as f:
            config = json.load(f)
            self.max_lines = int(config['max_lines'])
            self.from_conn = self.connectMysql(config['from'])
            self.to_conn = self.connectMysql(config['to'])
            self.from_db = config['from']['db']
            self.to_db = config['to']['db']
            self.logFile("sss")

    #       链接db
    def connectMysql(self, conf):
        return pymysql.connect(
            host = conf['host'],
            user = conf['user'],
            passwd = conf['passwd'],
            db = conf['db'],
            charset = conf['charset']
        )

    #   同步
    def dbSyn(self):
        #   读取源数据库表
        cur = self.from_conn.cursor()
        cur_local = self.to_conn.cursor()
        cur.execute('show tables')
        tables = cur.fetchall()

        for table ,*_ in tables:
            # 需要迁移的数据库查询表的列数
            cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE table_schema='" + self.from_db + "' AND table_name='" + table + "'")
            table_col_count, *_ = cur.fetchone()

            # # 需要迁移的数据库查询表的结构
            cur.execute('show create table ' + table)
            result = cur.fetchall()
            create_sql = result[0][1]

            # 创建表
            cur_local.execute("SELECT table_name FROM information_schema.`TABLES` WHERE table_schema='" + self.to_db + "' AND table_name='" + str(table).lower() + "'")
            table_name = cur_local.fetchone()
            if table_name is None:
                cur_local.execute(create_sql)


            if self.max_lines > 0:
                #   逐条数据迁移
                while True:
                    try:
                        #   根据限制获取数据
                        limit_param = ' limit ' + str(self.max_lines)
                        cur.execute('select * from ' + table + limit_param)
                        inserts = cur.fetchall()

                        param = ''
                        for i in range(0, table_col_count):
                            param = param + '%s,'
                        # 插入数据
                        cur_local.executemany('replace into ' + table + ' values (' + param[0:-1] + ')', inserts)
                        self.to_conn.commit()
                        break
                    except Exception as e:
                        logFile(str(e))
                        time.sleep(60)
                        cur = self.from_conn.cursor()
                        cur_local = self.to_conn.cursor()
            else:
                # 查询需要迁移的数据库表的数据条数
                cur.execute('select count(*) from ' + table)
                total ,*_ = cur.fetchone()

                page = total / self.page_size
                page1 = total % self.page_size
                if page1 != 0:
                    page = page + 1
                for p in range(0, int(page)):
                    while True:
                        try:
                            if p == 0:
                                limit_param = ' limit ' + str(p * self.page_size) + ',' + str(self.page_size)
                            else:
                                limit_param = ' limit ' + str(p * self.page_size + 1) + ',' + str(self.page_size)
                            cur.execute('select * from ' + table + limit_param)
                            inserts = cur.fetchall()
                            param = ''
                            for i in range(0, table_col_count):
                                param = param + '%s,'
                            cur_local.executemany('replace into ' + table + ' values (' + param[0:-1] + ')', inserts)
                            conn_local.commit()
                            break
                        except Exception as e:
                            logFile(str(e))
                            time.sleep(60)
                            cur = conn.cursor()
                            cur_local = conn_local.cursor()
        cur_local.close()
        self.to_conn.close()
        cur.close()
        self.from_conn.close()

    #   错误信息
def logFile(self, msg):
    with open('log.log', 'a') as f:
        f.write(str(int(time.time())) +":"+ msg)

if __name__ == '__main__':
    conn_mysql = MysqlSyn()
    conn_mysql.dbSyn()
