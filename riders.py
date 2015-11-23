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
                        BIKENO integer NOT NULL
                        )"""    #NUM is index
            cursor.execute(query)
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS STATS (
                        NUM serial PRIMARY KEY,
                        YEARS integer DEFAULT 0,
                        WINS integer DEFAULT 0,
                        PODIUM integer DEFAULT 0,
                        POLE integer DEFAULT 0,
                        CHAMP integer DEFAULT 0,
                        TOTALP integer DEFAULT 0,
                        BIKENO integer NOT NULL
                        )"""    #NUM is index
            cursor.execute(query)
        return

    def load_riders(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RIDERS"
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)

    def load_stats(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM STATS"
            cursor.execute(query)
            stats = cursor.fetchall()
        return (stats)

    def add_rider_default(self, name, surname, age, gender, team, brand, model, nation, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, BIKENO)    VALUES
                        ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', %s )""" % (name, surname, age, gender, team, brand, model, nation, bikeno)
            cursor.execute(query)
            connection.commit()
        return

    def add_stats_default(self, years, wins, podium, pole, champ, totalp, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO STATS (YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP, BIKENO)    VALUES
                        ( %s, %s, %s, %s, %s, %s , %s)""" % (years, wins, podium, pole, champ, totalp, bikeno)
            cursor.execute(query)
            connection.commit()
        return

    def del_rider_default(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NAME = '%s'
                        AND SURNAME = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
        return

    def del_stats_default(self, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM STATS WHERE BIKENO = %s """ % (bikeno)
            cursor.execute(query)
            connection.commit()
        return

    def del_rider_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

    def del_stats_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM STATS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return
    
    def update_rider_by_num(self, num, name, surname, age, gender, team, brand, model, nation, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  RIDERS
                        SET NAME = '%s', SURNAME = '%s', AGE = %s, GENDER = '%s', TEAM = '%s', BRAND = '%s', MODEL = '%s', NATION = '%s', BIKENO = %s
                        WHERE NUM = '%s' """ % (name, surname, age, gender, team, brand, model, nation, bikeno, num)
            cursor.execute(query)
            connection.commit()
        return
    
    def update_stats_by_num(self, num, years, wins, podium, pole, champ, totalp, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  STATS
                        SET YEARS = %s, WINS = %s, PODIUM = %s, POLE = %s, CHAMP = %s, TOTALP = %s, BIKENO = %s
                        WHERE NUM = '%s' """ % (years, wins, podium, pole, champ, totalp, bikeno, num)
            cursor.execute(query)
            connection.commit()
        return