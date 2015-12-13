import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Teams:
    searchName = ''
    searchCountry = ''
    searchConstructor = ''
    searchMotorcycle = ''

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

        return render_template('teams.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM teams WHERE name LIKE '%s'
            AND country LIKE '%s' AND constructor LIKE '%s'
            AND motorcycle LIKE '%s' ORDER BY id ASC""" % (('%' + Teams.searchName + '%'),
            ('%' + Teams.searchCountry + '%'),('%' + Teams.searchConstructor + '%'),
            ('%' + Teams.searchMotorcycle + '%'))

            Teams.searchName = ''
            Teams.searchCountry = ''
            Teams.searchConstructor = ''
            Teams.searchMotorcycle = ''

            cursor.execute(query)

            teamsdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('teams.html', teams = teamsdb, current_time=now.ctime())

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
        return redirect(url_for('teamsPage'))

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

    def addTeam(self, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s)""" % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

    def updateTeam(self, id, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE teams
                        SET name = '%s', country = '%s', constructor = '%s', motorcycle = '%s', riderNo = %s
                        WHERE id = '%s' """ % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo, id)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

    def deleteTeamId(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM teams WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('teamsPage'))

    def searchTeam(self, name, country, constructor, motorcycle):
        Teams.searchName = name.upper()
        Teams.searchCountry = country.upper()
        Teams.searchConstructor = constructor.upper()
        Teams.searchMotorcycle = motorcycle.upper()
        return redirect(url_for('teamsPage'))

