import psycopg2 as dbapi2

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Teams:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def openPage(self):
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

            query = "SELECT * FROM teams"
            cursor.execute(query)
            teamsdb = cursor.fetchall()
        return render_template('teams.html', teams = teamsdb)

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