import pymysql
from enum import IntEnum, unique

class mysql():
    def __init__(self):
        self.cur = 0
    conn = pymysql.connect(
        host    = 'localhost',
        port    = 3306,
        user    = 'root',
        passwd  = '',
        db      = 'novel_information_list',
        charset = 'utf8',
    )
    #连接Mysql数据库
    def connecttoMYSQL(self):
        self.cur = self.conn.cursor()
        return

    #断开Mysql数据库
    def disconnecttoMYSQL(self):
        self.cur = self.conn.commit()
        return

    '''
    Class    :   sql()数据库调用类
    Parameter:   str_bookid, int_type     , str_bookname, int_serialize,
                 str_author, str_novel_url, str_summary
    Function :   addNoveltoMYSQL()
    Effect   :   向novel_information_list表中插入
                 id, 书名， 类型， 连载状态， 作者， url链接， 简介
    Return   :   无
    '''
    # 参数顺序和Novel_Info的枚举一一对应
    def addNoveltoMYSQL(self, str_bookid, int_type, str_bookname, int_serialize,
                        str_author, str_novel_url, str_summary):
        print(str_bookid)
        print(int_type)
        print(str_bookname)
        print(int_serialize)
        print(str_author)
        print(str_novel_url)
        print(str_summary)
        self.connecttoMYSQL()
        print("导入数据库novel_information_list")
        self.cur.execute(
            "insert into " \
            "novel_information_list(novel_id,  type, novel_name, serialize, author, url, summary) " \
            "values('%d', '%d', '%s', '%d', '%s', '%s', '%s')"
            % (str_bookid, int_type, str_bookname, int_serialize, str_author, str_novel_url, str_summary)
        )
        self.disconnecttoMYSQL()
        return

    '''
    Class    :   sql()数据库调用类
    Parameter:   int_type, str_bookid, str_bookname, str_chaptername, str_content
    Function :   addchaptertoMYSQL()
    Effect   :   向novel_(int_type)_chapter表中插入
                 id, 书名， 章节， 内容
    Return   :   无
    '''
    def addchaptertoMYSQL(self, int_type, str_bookid, str_bookname, str_chaptername, str_content):
        print("导入数据库novel_chapter===========")
        self.connecttoMYSQL()
        table = "novel_%d_chapter" % (int_type)
        print(table)
        self.cur.execute(
            "insert into novel_%d_chapter" \
            "(novel_id, novel_name, novel_chapter_name, chapter_content)" \
            "values('%d', '%s', '%s', '%s')" %
            ( int_type,
              str_bookid, str_bookname, str_chaptername, str_content)
        )
        self.disconnecttoMYSQL()
        return


sql = mysql()