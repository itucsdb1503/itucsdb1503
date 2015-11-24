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
                        constructor text REFERENCES brands(name))"""
            cursor.execute(query)
            
            
            query = """SELECT * FROM models WHERE name LIKE '%s' ORDER BY ID ASC""" % (('%' + Model.searchName + '%'))
            Model.searchName = ''

            cursor.execute(query)

            modelsdb = cursor.fetchall()
        return render_template('models.html', models = modelsdb)


    def addModel(self, name, constructor):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO models (name, constructor)
                        VALUES
                        ('%s', '%s')""" % (name, constructor)
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
    
    def update(self, ID, name, constructor):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  models SET name = '%s', constructor = '%s' WHERE ID = '%s' """ % (name, constructor, ID)
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
                 
            query = """INSERT INTO models (name, constructor)
                        VALUES
                        ('Honda', 1),
                        ('Yamaha', 2),
                        ('MV Agusta', 3),
                        ('Aprilia', 4),
                        ('BMW', 5),
                        ('Suzuki', 6)"""

            connection.commit()
        return redirect(url_for('modelsPage'))
