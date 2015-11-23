import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class ridersClass:
    def __init__(self,dsn):
        self.dsn = dsn
        self.init()
        return

    def init(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS RIDERS (
                        NUM serial PRIMARY KEY,
                        NAME text NOT NULL,
                        SURNAME text NOT NULL,
                        AGE integer DEFAULT 0,
                        GENDER text NOT NULL,
                        TEAM text NOT NULL,
                        BRAND text NOT NULL,
                        MODEL text NOT NULL,
                        NATION text NOT NULL,
                        YEARS integer NOT NULL,
                        BIKENO integer UNIQUE
                        )"""    #NUM is index
            cursor.execute(query)
        return
    def fill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
                        VALUES
                        ('Valentino', 'Rossi', 36, 'Male', 'Movistar Yamaha MotoGP', 'Yamaha', 'Urbino', 'Italy', 15, 46) ,
                        ('Dani', 'Pedrosa', 30, 'Male','Repsol Honda Team', 'Honda', 'Sabadel', 'Spain', 9, 26)"""
            cursor.execute(query)
        return

    def load_riders(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RIDERS ORDER BY NUM ASC"
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)

    def add_rider_default(self, name, surname, age, gender, team, brand, model, nation, years, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)    VALUES
                        ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', %s, %s )""" % (name, surname, age, gender, team, brand, model, nation, years, bikeno)
            cursor.execute(query)
            connection.commit()
        return

    def del_rider_default(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NAME = '%s'
                        AND SURNAME = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
        return

    def del_rider_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

    def update_rider_by_num(self, num, name, surname, age, gender, team, brand, model, nation, years, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  RIDERS
                        SET NAME = '%s', SURNAME = '%s', AGE = %s, GENDER = '%s', TEAM = '%s', BRAND = '%s', MODEL = '%s', NATION = '%s', YEARS = %s, BIKENO = %s
                        WHERE NUM = '%s' """ % (name, surname, age, gender, team, brand, model, nation, years, bikeno, num)
            cursor.execute(query)
            connection.commit()
        return
    
    def search_rider_by_namesurname(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
        return
