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
                        country text NOT NULL)"""
            cursor.execute(query)
            
            
            query = """SELECT * FROM models WHERE name LIKE '%s' ORDER BY ID ASC""" % (('%' + Model.searchName + '%'))
            Model.searchName = ''

            cursor.execute(query)

            modelsdb = cursor.fetchall()
        return render_template('models.html', models = modelsdb)


    def addModel(self, name, country):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO models (name, country)
                        VALUES
                        ('%s', '%s')""" % (name, country)
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
    
    def update(self, ID, name, country):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  models SET name = '%s', country = '%s' WHERE ID = '%s' """ % (name, country, ID)
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
                 
            query = """INSERT INTO models (name, country)
                        VALUES
                        ('Honda', 'Japan'),
                        ('Yamaha', 'Japan'),
                        ('MV Agusta', 'Italy'),
                        ('Aprilia', 'Italy'),
                        ('BMW', 'Germany'),
                        ('Suzuki', 'Japan')"""

            connection.commit()
        return redirect(url_for('modelsPage'))
