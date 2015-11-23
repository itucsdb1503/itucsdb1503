import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class statsClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS STATS (
                        NUM serial PRIMARY KEY,
                        YEARS integer DEFAULT 0,
                        WINS integer DEFAULT 0,
                        PODIUM integer DEFAULT 0,
                        POLE integer DEFAULT 0,
                        CHAMP integer DEFAULT 0,
                        TOTALP integer DEFAULT 0,
                        BIKENO integer UNIQUE
                        )"""    #NUM is index
            cursor.execute(query)
        return

    def fill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO STATS (YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP, BIKENO)
                        VALUES
                        (15, 86, 175, 51, 7, 3942, 46),
                        (9, 28, 100, 28, 0, 2488, 26) """
            cursor.execute(query)
        return

    def load_stats(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM STATS"
            cursor.execute(query)
            stats = cursor.fetchall()
        return (stats)


    def add_stats_default(self, years, wins, podium, pole, champ, totalp, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO STATS (YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP, BIKENO)    VALUES
                        ( %s, %s, %s, %s, %s, %s , %s)""" % (years, wins, podium, pole, champ, totalp, bikeno)
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

    def del_stats_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM STATS WHERE NUM = '%s' """ % (num)
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
