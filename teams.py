import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Teams:
    searchName = ''

    def __init__(self, dsn):
        self.dsn = dsn
        return

    def createTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS teams (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        country text REFERENCES countries(abbreviation) ON DELETE RESTRICT ON UPDATE CASCADE,
                        constructor text NOT NULL,
                        motorcycle text NOT NULL,
                        riderNo integer DEFAULT 0)"""
            cursor.execute(query)

        return render_template('teams.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM teams WHERE name LIKE '%s' ORDER BY id ASC""" % (('%' + Teams.searchName + '%'))
            Teams.searchName = ''

            cursor.execute(query)

            teamsdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('teams.html', teams = teamsdb, current_time=now.ctime())

    def initTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            self.createTable()

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('DUCATI TEAM', 'ITA', 'DUCATI', 'DUCATI DESMOSEDICI GP15', 3),
                        ('REPSOL HONDA TEAM', 'JPN', 'HONDA', 'HONDA RC213V', 3),
                        ('AB MOTORACING', 'CZE', 'HONDA', 'HONDA RC213V-RS', 5),
                        ('E-MOTION IODARACING TEAM', 'ITA', 'ART', 'ART', 3),
                        ('MOVISTAR YAMAHA MOTOGP', 'JPN', 'YAMAHA', 'YAMAHA YZR-M1', 2),
                        ('MONSTER YAMAHA TECH 3', 'FRA', 'YAMAHA', 'YAMAHA YZR-M1', 2)"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('teamsPage'))

    def dropTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS teams"""
            cursor.execute(query)

            connection.commit()

    def addTeam(self, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s)""" % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo.upper())
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

    def updateTeam(self, id, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  teams
                        SET name = '%s', country = '%s', constructor = '%s', motorcycle = '%s', riderNo = %s
                        WHERE id = '%s' """ % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo.upper(), id)
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

    def searchTeamName(self, name):
        Teams.searchName = name.upper()
        return redirect(url_for('teamsPage'))

