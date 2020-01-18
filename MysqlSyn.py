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
        scritp, config_path = sys.argv
        self.config = None        #   配置数组
        self.timer_connet = 0     #   尝试链接计数
        self.from_conn = None
        self.to_conn = None
        self.loadConf(config_path);

    #   配置文件读取
    def loadConf(self, config_path):
        path = config_path
        with open(path, encoding='utf-8') as f:
            config = json.load(f)
            self.config = config
            self.timer_connet = 0
            self.from_conn = self.connectMysql(config['from'])
            self.timer_connet = 0
            self.to_conn = self.connectMysql(config['to'])

    #       链接db
    def connectMysql(self, conf):

        self.timer_connet += 1

        try:
            con = pymysql.connect(
                host = conf['host'],
                user = conf['user'],
                passwd = conf['passwd'],
                db = conf['db'],
                charset = conf['charset']
            )
        except Exception as e:
            #   最大重连次数
            if self.timer_connet >= 5:
                logFile("连接数据库失败")
                sys.exit()
            else:
                #   尝试重连
                sleeptime = self.timer_connet * 60
                time.sleep(sleeptime)
                self.connectMysql(conf)
        return con

    #   同步
    def dbSyn(self):
        #   读取源数据库表
        cur = self.from_conn.cursor()
        cur_local = self.to_conn.cursor()
        cur.execute('show tables')
        tables = cur.fetchall()

        for table ,*_ in tables:
            # 需要迁移的数据库查询表的列数
            cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE table_schema='" + self.config['from']['db'] + "' AND table_name='" + table + "'")
            table_col_count, *_ = cur.fetchone()

            # # 需要迁移的数据库查询表的结构
            cur.execute('show create table ' + table)
            result = cur.fetchall()
            create_sql = result[0][1]

            #   视图跳过
            if "ALGORITHM" in create_sql:
                continue

            # 创建表
            cur_local.execute("SELECT table_name FROM information_schema.`TABLES` WHERE table_schema='" + self.config['to']['db'] + "' AND table_name='" + str(table).lower() + "'")
            table_name = cur_local.fetchone()
            if table_name is None:
                cur_local.execute(create_sql)


            # 查询需要迁移的数据库表的数据条数
            cur.execute('select count(*) from ' + table)
            total ,*_ = cur.fetchone()

            #   根据配置获得实际迁移条目
            if table in self.config['custom']:
                total = int(self.config['custom'][table])
            else:
                if int(self.config['default_max_lines']) > 0:
                    total = int(self.config['default_max_lines'])


            page_size = int(self.config['page_size'])
            page = total / page_size
            page1 = total % page_size
            if page1 != 0:
                page = page + 1
            for p in range(0, int(page)):
                while True:
                    try:
                        #   获取数据
                        if total > page_size:
                            if p == 0:
                                limit_param = ' limit ' + str(p * page_size) + ',' + str(page_size)
                            else:
                                limit_param = ' limit ' + str(p * page_size + 1) + ',' + str(page_size)
                        else:
                            limit_param = ' limit ' + str(total)
                        cur.execute('select * from ' + table + limit_param)
                        inserts = cur.fetchall()

                        #   插入数据
                        param = ''
                        for i in range(0, table_col_count):
                            param = param + '%s,'
                        cur_local.executemany('replace into ' + table + ' values (' + param[0:-1] + ')', inserts)
                        self.to_conn.commit()
                        break
                    except Exception as e:
                        logFile(str(e))
                        time.sleep(60)
                        cur = self.from_conn.cursor()
                        cur_local = self.to_conn.cursor()
        cur_local.close()
        self.to_conn.close()
        cur.close()
        self.from_conn.close()

    #   错误信息
def logFile( msg):
    with open('log.log', 'a') as f:
        f.write(str(int(time.time())) +":"+ msg)

if __name__ == '__main__':
    conn_mysql = MysqlSyn()
    conn_mysql.dbSyn()
