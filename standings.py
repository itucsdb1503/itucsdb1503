import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class standings:
    searchName = ''
    searchPoints = -1

    def __init__(self, dsn):
        self.dsn = dsn
        return

    def createTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS standings (
                        position integer PRIMARY KEY,
                        name text UNIQUE REFERENCES teams(name) ON UPDATE CASCADE ON DELETE CASCADE,
                        points integer DEFAULT 0)"""
            cursor.execute(query)

        return render_template('standings.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            if standings.searchPoints == -1:
                query = """SELECT * FROM standings WHERE name LIKE '%s'
                ORDER BY position ASC""" % (('%' + standings.searchName + '%'))

            else:
                query = """SELECT * FROM standings WHERE name LIKE '%s'
                AND points = %s ORDER BY position ASC""" % (('%' + standings.searchName + '%'),
                (standings.searchPoints))

            standings.searchName = ''
            standings.searchPoints = -1

            cursor.execute(query)

            standingsdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('standings.html', standings = standingsdb, current_time=now.ctime())

    def initTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            self.createTable()

            query = """INSERT INTO standings (position, name, points)
                        VALUES
                        (2, 'REPSOL HONDA TEAM', 453),
                        (3, 'DUCATI TEAM', 350),
                        (14, 'AB MOTORACING', 0),
                        (1, 'MOVISTAR YAMAHA MOTOGP', 655),
                        (10, 'ATHINA FORWARD RACING', 39),
                        (11, 'APRILIA RACING TEAM GRESINI', 39),
                        (4, 'MONSTER YAMAHA TECH 3', 295)"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('standingsPage'))

    def dropTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS standings"""
            cursor.execute(query)

            connection.commit()

    def addstanding(self, position, name, points):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO standings (position, name, points)
                        VALUES
                        (%s, '%s', %s)""" % (position, name.upper(), points)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('standingsPage'))

    def updatestanding(self, position, name, points):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE standings
                        SET name = '%s', points = %s
                        WHERE position = %s """ % (name.upper(), points, position)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('standingsPage'))

    def deletestanding(self, position):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM standings WHERE position = %s """ % (position)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('standingsPage'))

    def searchstanding(self, name, points):
        standings.searchName = name.upper()
        if points == '':
            standings.searchPoints = -1
        else:
            standings.searchPoints = points
        return redirect(url_for('standingsPage'))

