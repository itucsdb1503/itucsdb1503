import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class ridersClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS RIDERS (
                        NUM serial PRIMARY KEY,
                        NAME text NOT NULL,
                        SURNAME text NOT NULL,
                        AGE integer DEFAULT 0,
                        GENDER text NOT NULL,
                        TEAM text NOT NULL,
                        BRAND text NOT NULL,
                        MODEL text NOT NULL,
                        NATION text NOT NULL,
                        YEARS integer DEFAULT 0,
                        WINS integer DEFAULT 0,
                        PODIUM integer DEFAULT 0,
                        POLE integer DEFAULT 0,
                        CHAMP integer DEFAULT 0,
                        TOTALP integer DEFAULT 0
                        )"""
            cursor.execute(query)
        return

    def load(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RIDERS"
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)

    def add_default(self, name, surname, age, gender, team, brand, model, nation, years, wins, podium, pole, champ, totalp):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP)    VALUES
                        ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s )""" % (name, surname, age, gender, team, brand, model, nation, years, wins, podium, pole, champ, totalp)
            cursor.execute(query)
            connection.commit()
        return
    
    def del_default(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NAME = '%s'
                        AND SURNAME = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
            
        return 
    
    def del_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return