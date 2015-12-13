import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class personalClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS PERSONAL (
                        NUM serial PRIMARY KEY,
                        BIRTH DATE NULL,
                        WEIGHT INTEGER DEFAULT 0,
                        HEIGHT INTEGER DEFAULT 0,
                        FAVCIR TEXT,
                        WEBSITE TEXT,
                        FACEB TEXT,
                        TWIT TEXT,
                        INSTA TEXT,
                        FANS INTEGER DEFAULT 0,
                        PERSID serial UNIQUE REFERENCES RIDERS(NUM) ON DELETE CASCADE ON UPDATE CASCADE
                        )"""    #NUM is index
            cursor.execute(query)
        return

    def fill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PERSONAL (BIRTH, WEIGHT, HEIGHT, FAVCIR, WEBSITE, FACEB, TWIT, INSTA, FANS, PERSID)
                        VALUES
                        ('1979-02-16', 65, 182, 'FRA', 'www.valentinorossi.com', 'ValentinoRossiVR46Official', 'ValeYellow46', 'valeyellow46', 0, 1),
                        ('1985-09-29', 51, 160, 'ITA', 'www.danipedrosa.com', 'DaniPedrosaOfficial', '26_DaniPedrosa', '26_danipedrosa', 0, 2)"""
            cursor.execute(query)
        return

    def load_personal(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM PERSONAL ORDER BY FANS DESC"
            cursor.execute(query)
            detail = cursor.fetchall()
        return (detail)


    def add_personal_default(self, birth, weight, height, favcir, website, faceb, twit, insta, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PERSONAL (BIRTH, WEIGHT, HEIGHT, FAVCIR, WEBSITE, FACEB, TWIT, INSTA, FANS, PERSID)    VALUES
                        ( '%s', %s, %s, '%s', '%s', '%s' , '%s', '%s', 0, '%s')""" % (birth, weight, height, favcir, website, faceb, twit, insta, persid)
            cursor.execute(query)
            connection.commit()
        return

    def update_personal_by_rider(self, birth, weight, height, favcir, website, faceb, twit, insta, fans, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  YEARSTATS
                        SET BIRTH = '%s', WEIGHT = %s, HEIGHT = %s, FAVCIR = '%s', WEBSITE = '%s', FACEB = '%s', TWIT = '%s', INSTA = '%s', FANS = %s
                        WHERE PERSID = '%s' """ % (birth, weight, height, favcir, website, faceb, twit, insta, fans, persid)
            cursor.execute(query)
            connection.commit()
        return

    def search_personal_default(self, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM PERSONAL WHERE PERSID = '%s' ORDER BY FANS DESC""" % (persid)
            cursor.execute(query)
            detail = cursor.fetchall()
        return (detail)
    
    def del_personal_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

    def del_personal_by_rider(self, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE PERSID = '%s' """ % (persid)
            cursor.execute(query)
            connection.commit()
        return

    def inc_fans(self, num):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE PERSONAL SET FANS = FANS + 1 WHERE NUM = '%s'" % (num)
            cursor.execute(query)
            connection.commit()
        return
