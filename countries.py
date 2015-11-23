import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Countries:
    searchFlag = 0
    searchName = ''

    def __init__(self, dsn):
        self.dsn = dsn
        return

    def createTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS countries (
                        name text NOT NULL PRIMARY KEY,
                        abbreviation text NOT NULL,
                        continent text NOT NULL)"""
            cursor.execute(query)

        return render_template('countries.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            if Countries.searchFlag == 1:
                query = """SELECT * FROM countries WHERE name LIKE '%s' ORDER BY name ASC""" % ((Countries.searchName + '%'))
                Countries.searchFlag = 0
            else:
                query = "SELECT * FROM countries ORDER BY name ASC"

            cursor.execute(query)

            countriesdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('countries.html', countries = countriesdb, current_time=now.ctime())

    def addCountry(self, name, abbreviation, continent):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO countries (name, abbreviation, continent)
                        VALUES
                        ('%s', '%s', '%s')""" % (name.upper(), abbreviation.upper(), continent.upper())
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('countriesPage'))

    def updateCountry(self, name, newName, abbreviation, continent):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  countries
                        SET name = '%s', abbreviation = '%s', continent = '%s'
                        WHERE name = '%s' """ % (newName.upper(), abbreviation.upper(), continent.upper(), name.upper())
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('countriesPage'))

    def deleteCountryName(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM countries WHERE name = '%s' """ % (name.upper())
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('countriesPage'))

    def searchCountryName(self, name):
        Countries.searchFlag = 1
        Countries.searchName = name.upper()
        return redirect(url_for('countriesPage'))

    def listFullTable(self):
        Countries.searchFlag = 0
        return redirect(url_for('countriesPage'))

