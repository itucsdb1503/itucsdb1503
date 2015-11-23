import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class Race:
    search_bool=0;
    search_name='';
    def __init__(self, dsn):
        self.dsn = dsn
        return
    def search_race(self, name):
        with dbapi2.connect(self.dsn) as connection:
            Race.search_bool=1;
            Race.search_name=name.upper();
        return redirect(url_for('races_page'))
    def list_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS races (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        fastest_lap_time integer DEFAULT 0,
                        winners_average_lap_time integer DEFAULT 0,
                        average_lap_time integer DEFAULT 0,
                        first_position serial REFERENCES circuits(id),
                        track_circuit_id text NOT NULL,
                        number_of_laps integer DEFAULT 0,
                        total_accidents integer DEFAULT 0)"""
            cursor.execute(query)
            if Race.search_bool==1 :
                query = "SELECT * FROM races WHERE name LIKE '%s' ORDER BY id ASC" % (('%' + Race.search_name + '%'))
                cursor.execute(query)
                races = cursor.fetchall()
                Race.search_bool=0;
                return render_template('races.html', races = races)
            elif Race.search_bool==0 :
                query = "SELECT * FROM races ORDER BY id ASC"
                cursor.execute(query)
                races = cursor.fetchall()
                return render_template('races.html', races = races)

    def delete_race_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM races WHERE id = '%s' " % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('races_page'))
    def update_race(self, name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id, number_of_laps, total_accidents, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE  races SET name = '%s', fastest_lap_time = %s, winners_average_lap_time = %s, average_lap_time = %s, first_position = '%s', track_circuit_id = %s, number_of_laps = %s, total_accidents = %s
                        WHERE id = '%s' """ % (name.upper(), fastest_lap_time, winners_average_lap_time, average_lap_time, first_position.upper(), track_circuit_id, number_of_laps, total_accidents, id)

            cursor.execute(query)

            connection.commit()
        return redirect(url_for('races_page'))
    def add_race(self, name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id, number_of_laps, total_accidents):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO races (name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id, number_of_laps, total_accidents)
                        VALUES
                        ('%s', %s, %s, %s, '%s', %s, %s, %s)""" % (name.upper(), fastest_lap_time, winners_average_lap_time, average_lap_time, first_position.upper(), track_circuit_id, number_of_laps, total_accidents)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('races_page'))

