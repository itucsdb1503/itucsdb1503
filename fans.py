import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class fansClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:  
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS FANS (
                        NUM serial PRIMARY KEY,
                        NAME TEXT NOT NULL,
                        SURNAME TEXT NOT NULL,
                        MAIL TEXT NOT NULL,
                        BIRTH DATE NULL,
                        FANSID integer UNIQUE REFERENCES PERSONAL(NUM)
                        )"""    #NUM is index
            cursor.execute(query)
        return

    def load_fans(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM FANS ORDER BY NUM ASC"
            cursor.execute(query)
            fans = cursor.fetchall()
        return (fans)


    def add_fans_default(self, name, surname, mail, birth, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO FANS (NAME, SURNAME, MAIL, BIRTH, FANSID)    VALUES
                        ( '%s', '%s', '%s', '%s', '%s')""" % (name, surname, mail, birth, fansid)
            cursor.execute(query)
            connection.commit()
            cursor = connection.cursor()
            query = "UPDATE PERSONAL SET FANS = FANS + 1 WHERE NUM = '%s'" % (fansid)
            cursor.execute(query)
            connection.commit()
        return

    def update_fans_by_mail(self, name, surname, mail, birth, cmail):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  FANS
                        SET NAME = '%s', SURNAME = '%s', MAIL = '%s', BIRTH = '%s'
                        WHERE MAIL LIKE '%s' """ % (name, surname, mail, birth, ('%'+cmail+'%'))
            cursor.execute(query)
            connection.commit()
        return
    
    def update_fans_by_num(self, num, name, surname, mail, birth, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  FANS
                        SET NAME = '%s', SURNAME = '%s', MAIL = '%s', BIRTH = '%s', FANSID = '%s'
                        WHERE NUM = '%s' """ % (name, surname, mail, birth, fansid, num)
            cursor.execute(query)
            connection.commit()
        return

    def search_fans_default(self, name, surname, mail, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            if not fansid :
                query = """SELECT * FROM FANS WHERE NAME LIKE '%s' AND SURNAME LIKE '%s' AND MAIL LIKE '%s'
                ORDER BY NUM ASC""" % (('%'+name+'%'),('%'+surname+'%'),('%'+mail+'%'))
            else:
                query = """SELECT * FROM FANS WHERE NAME LIKE '%s' AND SURNAME LIKE '%s' AND MAIL LIKE '%s' AND FANSID = '%s'
                ORDER BY NUM ASC""" % (('%'+name+'%'),('%'+surname+'%'),('%'+mail+'%'),fansid)
            cursor.execute(query)
            fans = cursor.fetchall()
        return (fans)
    
    def del_fans_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FANS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

    def del_fans_by_mail(self, mail):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE MAIL = '%s' """ % (mail)
            cursor.execute(query)
            connection.commit()
        return