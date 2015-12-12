import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Accidents:
    search_bool=0;
    search_rider_name='';
    def __init__(self, dsn):
        self.dsn = dsn
        return
    def search_Accident(self, rider_name):
        with dbapi2.connect(self.dsn) as connection:
            Accidents.search_bool=1;
            Accidents.search_rider_name=rider_name.upper();
        return redirect(url_for('Accidents_page'))
    def list_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS Accident (
                         id serial PRIMARY KEY,
                        rider_name text NOT NULL,
                        rider_surname text NOT NULL,
                        race_id serial REFERENCES races(id),
                        is_fatal text NOT NULL)"""
            cursor.execute(query)
            if Accidents.search_bool==1 :
                query = "SELECT * FROM Accident WHERE rider_name LIKE '%s' ORDER BY id ASC" % (('%' + Accidents.search_rider_name + '%'))
                cursor.execute(query)
                Accident = cursor.fetchall()
                Accidents.search_bool=0;
                return render_template('accidents.html', Accident = Accident)
            elif Accidents.search_bool==0 :
                query = "SELECT * FROM Accident ORDER BY id ASC"
                cursor.execute(query)
                Accident = cursor.fetchall()
                return render_template('accidents.html', Accident = Accident)

    def delete_Accident_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM Accident WHERE id = '%s' " % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Accidents_page'))
    def update_Accident(self, rider_name, rider_surname, race_id, is_fatal, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  Accident SET rider_name = '%s', rider_surname = '%s', race_id = '%s', is_fatal = '%s'
            WHERE id = '%s' """ % (rider_name.upper(), rider_surname.upper(), race_id, is_fatal.upper(), id)

            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Accidents_page'))
    def add_Accident(self, rider_name, rider_surname, race_id, is_fatal):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor();
            query = """INSERT INTO Accident (rider_name, rider_surname, race_id, is_fatal)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (rider_name.upper(), rider_surname.upper(), race_id, is_fatal.upper())
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Accidents_page'))

