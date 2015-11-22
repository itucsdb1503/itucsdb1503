import psycopg2 as dbapi2
from flask import redirect
from flask import render_template
from flask.helpers import url_for

class riders:
    def load(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS RIDERS (
                        NUM serial PRIMARY KEY,
                        NAME text NOT NULL,
                        SURNAME text NOT NULL,
                        AGE integer,
                        GENDER test NOT NULL,
                        TEAM text NOT NULL,
                        BIKE text NOT NULL,
                        NATION text NOT NULL,
                        YEARS integer DEFAULT 0,
                        WINS integer DEFAULT 0,
                        PODIUM integer DEFAULT 0,
                        POLE integer DEFAULT 0,
                        CHAMP integer DEFAULT 0,
                        TOTALP integer DEFAULT 0
                        )"""
            cursor.execute(query)
            query = "SELECT * FROM RIDERS"
            cursor.execute(query)
            riders = cursor.fetchall()
        return render_template('riders.html', riders)