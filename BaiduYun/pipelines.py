#-*- encoding:utf-8 -*-
import time
from twisted.enterprise import adbapi
import MySQLdb, MySQLdb.cursors
from scrapy import log
import pymysql
from django.db import IntegrityError
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class BaiduyunPipeline(object):
    global a
    a = 0
    def __init__(self):
        #global a
        #a = datetime.now()
        '''self.conn = None
        self.filename = 'G://Spider//BaiduYunDjango//BaiduYun.db'
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)'''
        self.connect = pymysql.connect(host='127.0.0.1',
                                            db='baiduyun',
                                            user='root',
                                            passwd='root',
                                            charset='utf8',
                                            use_unicode=True
                                            )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        #print str(item['shareId']) +' '+item['title']+ '  ' + str(item['userId']) + ' ' + item['userName']
        self.cursor.execute('select * from cms_fileinfo where id = %s' % item['shareId'])
        ret1 = self.cursor.fetchone()
        if not ret1:
            try:
                self.cursor.execute('insert into cms_fileinfo(id,title,userId,addTime,hits,downloads) values(%s,%s,%s,%s,%s,%s);',
                              (item['shareId'], item['title'],item['userId'], time.time(), 0, 0))
            except IntegrityError:
                return item;
        self.cursor.execute('select * from cms_userinfo where id = %s' % item['userId'])
        ret2 = self.cursor.fetchone()
        if not ret2:
            try:
                self.cursor.execute('insert into cms_userinfo(id, userName, userUrl, userAvaUrl, hits) values(%s,%s,%s,%s,%s);',
                          (item['userId'],  item['userName'], item['userUrl'], item['userAvaUrl'], 0))
            except IntegrityError:
                return item;
        self.connect.commit()
        return item;


        #tx.commit()
    '''
    def finalize(self):
        global a
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            b = datetime.now()
            print 'cost ' + str((b-a).seconds) + ' s'
    '''


    '''
    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table CMS_fileinfo(id integer primary key,title
                   text, userId text, addTime text, hits integer, downloads integer)""")
        conn.execute("""create table CMS_userinfo(id integer primary key, userName text, userUrl text, userAvaUrl text, hits text)""")
        #conn.execute("""create table CMS_taginfo(id integer primary key autoincrement,tagName
        #           text, fileId text)""")
        conn.execute("""create table CMS_searchinfo(id integer primary key,searchText
                           text, searchCount text, searchTime text)""")
        conn.commit()
        return conn'''
