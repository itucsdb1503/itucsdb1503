import psycopg2 as dbapi2
from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Specification:
    searchModel = ''
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def list(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
                        
            query = """CREATE TABLE IF NOT EXISTS specifications (
                        ID serial PRIMARY KEY,
                        model text NOT NULL UNIQUE,
                        engine text NOT NULL,
                        fuel integer DEFAULT 0,
                        power integer DEFAULT 0,
                        speed integer DEFAULT 0,
                        weight integer DEFAULT 0)"""
            cursor.execute(query)
            
            
            query = """SELECT * FROM specifications WHERE model LIKE '%s' ORDER BY ID ASC""" % (('%' + Specification.searchModel + '%'))
            Specification.searchModel = ''

            cursor.execute(query)

            specificationsdb = cursor.fetchall()
        return render_template('specifications.html', specifications = specificationsdb)


    def addSpecification(self, model, engine, fuel, power, speed, weight):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO specifications (model, engine, fuel, power, speed, weight)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s', '%s')""" % (model, engine, fuel, power, speed, weight)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('specificationsPage'))

    def deletebyModel(self, model):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM specifications WHERE model = '%s' " % (model)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('specificationsPage'))
    
    def deletebyId(self, ID):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM specifications WHERE ID = '%s' " % (ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('specificationsPage'))
    
    def update(self, ID, model, engine, fuel, power, speed, weight):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  specifications SET model = '%s', engine = '%s', fuel = '%s', power = '%s', speed = '%s', weight = '%s'  
            WHERE ID = '%s' """ % (model, engine, fuel, power, speed, weight, ID)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('specificationsPage'))
    
    def deleteAll(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS specifications CASCADE"""
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('specificationsPage'))
    
    def autoFill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()   
             
            query = """DROP TABLE IF EXISTS specifications CASCADE"""
            cursor.execute(query)
            
            query1 = """CREATE TABLE IF NOT EXISTS specifications (
                        ID serial PRIMARY KEY,
                        model text NOT NULL UNIQUE,
                        engine text NOT NULL,
                        fuel integer DEFAULT 0,
                        power integer DEFAULT 0,
                        speed integer DEFAULT 0,
                        weight integer DEFAULT 0)"""
            cursor.execute(query1)            
                   
            query2 = """INSERT INTO specifications (model, engine, fuel, power, speed, weight)
                        VALUES
                        ('YZR-M1', '1,000 cc, Inline-4', 21, 183, 340, 157),
                        ('RC213V', '1,000 cc, four-stroke', 21, 176, 350, 160),
                        ('GP15', '1,000 cc, four-stroke', 21, 179, 340, 158),
                        ('GSX-RR', 'Japan', 24, 169, 330, 160)"""
            cursor.execute(query2)
            connection.commit()
        return redirect(url_for('specificationsPage'))
