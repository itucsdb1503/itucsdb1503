import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Teams:
    searchFlag = 0
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
                        country text NOT NULL,
                        constructor text NOT NULL,
                        motorcycle text NOT NULL,
                        riderNo integer DEFAULT 0)"""
            cursor.execute(query)

        return render_template('teams.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            if Teams.searchFlag == 1:
                query = """SELECT * FROM teams WHERE name LIKE '%s' ORDER BY id ASC""" % ((Teams.searchName + '%'))
                Teams.searchFlag = 0;
            else:
                query = "SELECT * FROM teams ORDER BY id ASC"

            cursor.execute(query)

            teamsdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('teams.html', teams = teamsdb, current_time=now.ctime())

    def insertTestTuples(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS teams"""
            cursor.execute(query)

            query = """CREATE TABLE teams (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        country text NOT NULL,
                        constructor text NOT NULL,
                        motorcycle text NOT NULL,
                        riderNo integer DEFAULT 0)"""
            cursor.execute(query)

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('DUCATI TEAM', 'ITALY', 'DUCATI', 'DUCATI DESMOSEDICI GP15', 3),
                        ('E-MOTION IODARACING TEAM', 'ITALY', 'ART', 'ART', 3),
                        ('REPSOL HONDA TEAM', 'JAPAN', 'HONDA', 'HONDA RC213V', 3),
                        ('AB MOTORACING', 'CZECH REPUBLIC', 'HONDA', 'HONDA RC213V-RS', 5)"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('teamsPage'))

    def addTeam(self, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s)""" % (name, country, constructor, motorcycle, riderNo)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

    def updateTeam(self, id, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  teams
                        SET name = '%s', country = '%s', constructor = '%s', motorcycle = '%s', riderNo = %s
                        WHERE id = '%s' """ % (name, country, constructor, motorcycle, riderNo, id)
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
        Teams.searchFlag = 1
        Teams.searchName = name
        return redirect(url_for('teamsPage'))

    def listFullTable(self):
        Teams.searchFlag = 0
        return redirect(url_for('teamsPage'))

