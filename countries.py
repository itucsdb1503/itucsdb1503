import psycopg2 as dbapi2
import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Countries:
    searchName = ''
    searchAbbreviation = ''
    searchContinent = ''

    def __init__(self, dsn):
        self.dsn = dsn
        return

    def createTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            query = """CREATE TABLE IF NOT EXISTS countries (
                        name text NOT NULL,
                        abbreviation text NOT NULL PRIMARY KEY,
                        continent text NOT NULL)"""
            cursor.execute(query)

        return render_template('countries.html')

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM countries WHERE name LIKE '%s'
            AND abbreviation LIKE '%s' AND continent LIKE '%s'
            ORDER BY name ASC""" % (('%' + Countries.searchName + '%'),
            ('%' + Countries.searchAbbreviation + '%'),('%' + Countries.searchContinent + '%'))

            Countries.searchName = ''
            Countries.searchAbbreviation = ''
            Countries.searchContinent = ''

            cursor.execute(query)

            countriesdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('countries.html', countries = countriesdb, current_time=now.ctime())

    def initTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            self.createTable()

            query = """INSERT INTO countries (name, abbreviation, continent)
                        VALUES
                        ('ITALY', 'ITA', 'EUROPE'),
                        ('JAPAN', 'JPN', 'ASIA'),
                        ('CZECH REPUBLIC', 'CZE', 'EUROPE'),
                        ('AUSTRALIA', 'AUS', 'NORTH AMERICA'),
                        ('FRANCE', 'FRA', 'EUROPE'),
                        ('UNITED STATES OF AMERICA', 'USA', 'NORTH AMERICA'),
                        ('SPAIN', 'ESP', 'EUROPE'),
                        ('COLOMBIA', 'COL', 'SOUTH AMERICA')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('countriesPage'))

    def dropTable(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS countries CASCADE"""
            cursor.execute(query)

            connection.commit()

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

    def searchCountry(self, name, abbreviation, continent):
        Countries.searchName = name.upper()
        Countries.searchAbbreviation = abbreviation.upper()
        Countries.searchContinent = continent.upper()
        return redirect(url_for('countriesPage'))

