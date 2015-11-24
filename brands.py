import psycopg2 as dbapi2
from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Brand:
    searchName = ''
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def list(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            
            query = """CREATE TABLE IF NOT EXISTS brands (
                        ID serial PRIMARY KEY,
                        name text NOT NULL,
                        country text NOT NULL,
                        year integer DEFAULT 0,
                        champion integer DEFAULT 0)"""
            cursor.execute(query)
            
            
            query = """SELECT * FROM brands WHERE name LIKE '%s' ORDER BY ID ASC""" % (('%' + Brand.searchName + '%'))
            Brand.searchName = ''

            cursor.execute(query)

            brandsdb = cursor.fetchall()
        return render_template('brands.html', brands = brandsdb)


    def addBrand(self, name, country, year, champion):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO brands (name, country, year, champion)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (name, country, year, champion)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))

    def deletebyName(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM brands WHERE name = '%s' " % (name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('brandsPage'))
    
    def deletebyId(self, ID):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM brands WHERE ID = '%s' " % (ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('brandsPage'))
    
    def update(self, ID, name, country, year, champion):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  brands SET name = '%s', country = '%s', year = '%s', champion = '%s'  WHERE ID = '%s' """ % (name, country, year, champion, ID)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))
    
    def deleteAll(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS brands"""
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))
    
    def autoFill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()   
                   
            query = """INSERT INTO brands (name, country)
                        VALUES
                        ('Honda', 'Japan'),
                        ('Yamaha', 'Japan'),
                        ('MV Agusta', 'Italy'),
                        ('Aprilia', 'Italy'),
                        ('BMW', 'Germany'),
                        ('Suzuki', 'Japan')"""
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))
