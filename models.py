import psycopg2 as dbapi2
from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Model:
    searchName = ''
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def list(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            
            query = """CREATE TABLE IF NOT EXISTS models (
                        ID serial PRIMARY KEY,
                        name text NOT NULL,
                        rider text NOT NULL,
                        constructor text REFERENCES brands(name))"""
            cursor.execute(query)
            
            
            query = """SELECT * FROM models WHERE name LIKE '%s' ORDER BY ID ASC""" % (('%' + Model.searchName + '%'))
            Model.searchName = ''

            cursor.execute(query)

            modelsdb = cursor.fetchall()
        return render_template('models.html', models = modelsdb)


    def addModel(self, name, rider, constructor):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO models (name, rider, constructor)
                        VALUES
                        ('%s', '%s', '%s')""" % (name, rider, constructor)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('modelsPage'))

    def deletebyName(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM models WHERE name = '%s' " % (name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('modelsPage'))
    
    def deletebyId(self, ID):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM models WHERE ID = '%s' " % (ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('modelsPage'))
    
    def update(self, ID, name, rider, constructor):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  models SET name = '%s', rider = '%s', constructor = '%s' WHERE ID = '%s' """ % (name, rider, constructor, ID)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('modelsPage'))
    
    def deleteAll(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS models"""
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('modelsPage'))
    
    def autoFill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()   
             
            query = """DROP TABLE IF EXISTS models"""
            cursor.execute(query)
            
            query1 = """CREATE TABLE IF NOT EXISTS models (
                        ID serial PRIMARY KEY,
                        name text NOT NULL,
                        rider text NOT NULL,
                        constructor text REFERENCES brands(name))"""
            cursor.execute(query1)            
                   
            query2 = """INSERT INTO models (name, rider, constructor)
                        VALUES
                        ('RC213V', 'Dani Pedrosa', 'Honda'),
                        ('RC213V', 'Marc Marquez', 'Honda'),
                        ('RCV1000R', 'Hiroshi Aoyama', 'Honda'),
                        ('YZR-M1', 'Valentino Rossi', 'Yamaha'),
                        ('YZR-M1', 'Jorge Lorenzo', 'Yamaha'),
                        ('YZR-M1', 'Ben Spies', 'Yamaha'),
                        ('RS-GP', 'Marco Melandri', 'Aprilia'),
                        ('RS-GP', 'Alvaro Bautista', 'Aprilia'),
                        ('GSX-RR', 'Aleix Espargaro', 'Suzuki'),
                        ('GSX-RR', 'Maverick ViNales', 'Suzuki'),
                        ('GP15', 'Andrea Dovizioso', 'Ducati'),
                        ('GP15', 'Andrea Iannone', 'Ducati')"""
            cursor.execute(query2)
            connection.commit()
        return redirect(url_for('modelsPage'))
    