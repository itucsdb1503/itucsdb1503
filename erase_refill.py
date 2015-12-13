import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class reset_memmi:
    def __init__(self, dsn):
        self.dsn = dsn
        return
    def list_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS Accident"""
            cursor.execute(query)
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS races"""
            cursor.execute(query)
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS circuits"""
            cursor.execute(query)
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

            cursor = connection.cursor()
            query = """INSERT INTO circuits (name, length, width, left_corners, right_corners, longest_straight, country, constructed_year)
                        VALUES
                        ('Losail International Circuit', 5400, 12, 6, 10, 1068, 'Qatar', 2004) ,
                        ('Circuito de Jerez', 4400, 11, 5, 8, 607, 'Spain', 1985) ,
                        ('Le Mans', 4200, 13, 5, 9, 674, 'France', 1923) """
            cursor.execute(query)
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS races (
                         id serial PRIMARY KEY,
                        name text NOT NULL,
                        fastest_lap_time integer DEFAULT 0,
                        winners_average_lap_time integer DEFAULT 0,
                        average_lap_time integer DEFAULT 0,
                        first_position text NOT NULL ,
                        track_circuit_id serial REFERENCES circuits(id),
                        number_of_laps integer DEFAULT 0,
                        total_accidents integer DEFAULT 0)"""
            cursor.execute(query)
            cursor = connection.cursor()
            query = """INSERT INTO races (name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id , number_of_laps, total_accidents)
                        VALUES
                        ('Grand Prix of Qatar', 114, 118, 121, 'Valentino Rossi', 1, 22, 0) ,
                        ('Gran Premio de Espana', 98, 103, 105, 'Valentino Rossi', 2, 27, 1) ,
                        ('Grand Prix de France', 92, 95, 98, 'Jorge Lorenzo', 3, 28, 1) """
            cursor.execute(query)
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS Accident (
                         id serial PRIMARY KEY,
                        rider_name text NOT NULL,
                        rider_surname text NOT NULL,
                        race_id serial REFERENCES races(id),
                        is_fatal text NOT NULL)"""
            cursor.execute(query)

            cursor = connection.cursor()
            query = """INSERT INTO Accident (rider_name, rider_surname, race_id, is_fatal)
                        VALUES
                        ('Valentino', 'Rossi', 2, 'No')"""
            cursor.execute(query)
            return


