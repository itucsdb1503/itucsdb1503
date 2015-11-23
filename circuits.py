import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Circuit:
    search_bool=0;
    search_name='';
    def __init__(self, dsn):
        self.dsn = dsn
        return
    def search_circuit(self, name):
        with dbapi2.connect(self.dsn) as connection:
            Circuit.search_bool=1;
            Circuit.search_name=name;
        return redirect(url_for('circuits_page'))
    def list_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()


            query = """CREATE TABLE IF NOT EXISTS circuits (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        length integer DEFAULT 0,
                        width integer DEFAULT 0,
                        left_corners integer DEFAULT 0,
                        right_corners integer DEFAULT 0,
                        longest_straight integer DEFAULT 0,
                        country text NOT NULL,
                        constructed_year integer DEFAULT 0)"""
            cursor.execute(query)
            if Circuit.search_bool==1 :
                query = "SELECT * FROM circuits WHERE name = '%s' ORDER BY id ASC" % (Circuit.search_name)
                cursor.execute(query)
                circuits = cursor.fetchall()
                Circuit.search_bool=0;
                return render_template('circuits.html', circuits = circuits)
            elif Circuit.search_bool==0 :
                query = "SELECT * FROM circuits ORDER BY id ASC"
                cursor.execute(query)
                circuits = cursor.fetchall()
                return render_template('circuits.html', circuits = circuits)

    def delete_circuit_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM circuits WHERE id = '%s' " % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('circuits_page'))
    def update_circuit(self, name, length, width, left_corners, right_corners, longest_straight, country, constructed_year, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  circuits SET name = '%s', length = %s, width = %s, left_corners = %s, right_corners = %s, longest_straight = %s, country = '%s', constructed_year = %s
                        WHERE id = '%s' """ % (name.upper(), length, width, left_corners, right_corners, longest_straight, country.upper(), constructed_year, id)

            cursor.execute(query)

            connection.commit()
        return redirect(url_for('circuits_page'))
    def add_circuit(self, name, length, width, left_corners, right_corners, longest_straight, country, constructed_year):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO circuits (name, length, width, left_corners, right_corners, longest_straight, country, constructed_year)
                        VALUES
                        ('%s', %s, %s, %s, %s, %s, '%s', %s)""" % (name.upper(), length, width, left_corners, right_corners, longest_straight, country.upper(), constructed_year)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('circuits_page'))

