import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class yearstatsClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:    #####TODO: Prevent same STATID tuples to have same YEAR!!!!!!!!!!!!!!
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS YEARSTATS (
                        NUM serial PRIMARY KEY,
                        YEAR integer DEFAULT 0,
                        RACES integer DEFAULT 0,
                        VICTORY integer DEFAULT 0,
                        SECOND integer DEFAULT 0,
                        THIRD integer DEFAULT 0,
                        PODIUM integer DEFAULT 0,
                        POLE integer DEFAULT 0,
                        POINTS integer DEFAULT 0,
                        POSITION integer DEFAULT 0,
                        STATID serial REFERENCES RIDERS(NUM)
                        )"""    #NUM is index
            cursor.execute(query)
        return
 
    def fill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO YEARSTATS (YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)
                        VALUES
                        (2013, 16, 11, 2, 3, 16, 9, 178, 1, 1),
                        (2009, 18, 4, 9, 3, 16, 7, 127, 1, 1),
                        (2009, 16, 5, 4, 3, 12, 5, 87, 5, 2),
                        (2005, 17, 12, 3, 1, 16, 14, 246, 1, 1) """
            cursor.execute(query)
        return

    def load_stats(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM YEARSTATS ORDER BY NUM ASC"
            cursor.execute(query)
            stats = cursor.fetchall()
        return (stats)


    def add_stats_default(self, year, races, victory, second, third, podium, pole, points, position, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO YEARSTATS (YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)    VALUES
                        ( %s, %s, %s, %s, %s, %s , %s, %s, %s, '%s')""" % (year, races, victory, second, third, podium, pole, points, position, statid)
            cursor.execute(query)
            connection.commit()
        return

    def del_stats_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM YEARSTATS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return
    
    def del_stats_by_rider(self, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM YEARSTATS WHERE STATID = '%s' """ % (statid)
            cursor.execute(query)
            connection.commit()
        return

    def update_stats_by_num(self, num, year, races, victory, second, third, podium, pole, points, position, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  YEARSTATS
                        SET YEAR = %s, RACES = %s, VICTORY = %s, SECOND = %s, THIRD = %s, PODIUM = %s, POLE = %s, POINTS = %s, POSITION = %s, STATID = '%s'
                        WHERE NUM = '%s' """ % (year, races, victory, second, third, podium, pole, points, position, statid, num)
            cursor.execute(query)
            connection.commit()
        return
    
    def search_stats_default(self, year, position):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            if not year and not position:
                query = """SELECT * FROM YEARSTATS ORDER BY NUM ASC"""
            elif not year :
                query = """SELECT * FROM YEARSTATS WHERE POSITION = %s
                    ORDER BY NUM ASC""" % (position)
            elif not position:
                query = """SELECT * FROM YEARSTATS WHERE YEAR = %s ORDER BY NUM ASC""" % (year)
            else:
                query = """SELECT * FROM YEARSTATS WHERE YEAR = %s AND POSITION = %s ORDER BY NUM ASC""" % (year,position)
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)

    def search_stats_by_rider(self, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM YEARSTATS WHERE STATID = '%s' ORDER BY NUM ASC""" % (statid)
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)