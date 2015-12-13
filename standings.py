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

    def createTable(self):      #this create all 3 tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS countries (
                        name text NOT NULL,
                        abbreviation text NOT NULL PRIMARY KEY,
                        continent text NOT NULL)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS teams (
                        id serial PRIMARY KEY,
                        name text UNIQUE,
                        country text REFERENCES countries(abbreviation) ON DELETE RESTRICT ON UPDATE CASCADE,
                        constructor text NOT NULL,
                        motorcycle text NOT NULL,
                        riderNo integer DEFAULT 0)"""
            cursor.execute(query)

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

    def initTable(self):        #this initializes all 3 tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            self.createTable()

            query = """INSERT INTO countries (name, abbreviation, continent)
                        VALUES
                        ('ITALY', 'ITA', 'EUROPE'),
                        ('JAPAN', 'JPN', 'ASIA'),
                        ('CZECH REPUBLIC', 'CZE', 'EUROPE'),
                        ('AUSTRALIA', 'AUS', 'AUSTRALIA'),
                        ('SWITZERLAND', 'CHE', 'EUROPE'),
                        ('FRANCE', 'FRA', 'EUROPE'),
                        ('UNITED STATES OF AMERICA', 'USA', 'NORTH AMERICA'),
                        ('SPAIN', 'ESP', 'EUROPE'),
                        ('COLOMBIA', 'COL', 'SOUTH AMERICA')"""
            cursor.execute(query)

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('REPSOL HONDA TEAM', 'JPN', 'HONDA', 'RC213V', 3),
                        ('DUCATI TEAM', 'ITA', 'DUCATI', 'DESMOSEDICI GP15', 3),
                        ('AB MOTORACING', 'CZE', 'HONDA', 'RC213V-RS', 5),
                        ('MOVISTAR YAMAHA MOTOGP', 'JPN', 'YAMAHA', 'YZR-M1', 2),
                        ('ATHINA FORWARD RACING', 'CHE', 'YAMAHA', 'FORWARD', 4),
                        ('APRILIA RACING TEAM GRESINI', 'ITA', 'APRILIA', 'RS-GP', 4),
                        ('MONSTER YAMAHA TECH 3', 'FRA', 'YAMAHA', 'YZR-M1', 2)"""
            cursor.execute(query)

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

    def dropTable(self):        #This drops all three tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS countries CASCADE"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS teams CASCADE"""
            cursor.execute(query)

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

    def updatestanding(self, position, newPosition, name, points):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE standings
                        SET position = %s, name = '%s', points = %s
                        WHERE position = %s """ % (newPosition, name.upper(), points, position)
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

