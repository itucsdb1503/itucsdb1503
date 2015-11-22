import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import request
from flask import render_template
from flask.helpers import url_for
from flask import redirect

from riders import ridersClass
from teams import Teams

app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teams', methods=['GET', 'POST'])
def teamsPage():
    page = Teams(dsn = app.config['dsn'])
    if request.method == 'GET':
        page.createTable();
        #page.insertTestTuples();
        return page.loadPage()
    elif 'addTeam' in request.form:
        name = request.form['name']
        country = request.form['country']
        constructor = request.form['constructor']
        motorcycle = request.form['motorcycle']
        riderNo = request.form['riderNo']
        return page.addTeam(name, country, constructor, motorcycle, riderNo)
    elif 'deleteTeam' in request.form:
        id = request.form['id']
        return page.deleteTeamId(id)

@app.route('/riders', methods=['GET','POST'])
def riders():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'adddefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        AGE = request.form['age']
        GENDER = request.form['gender']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        YEARS = request.form['years']
        WINS = request.form['wins']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        CHAMP = request.form['champ']
        TOTALP= request.form['totalpoints']
        result.add_default(NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP)
    if 'deldefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        result.del_default(NAME, SURNAME)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_by_num(NUM)
    return render_template('/riders.html', result=result.load(), current_time=now.ctime())   

@app.route('/riders/list', methods=['GET','POST'])
def rlist():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    return render_template('/riders/list.html', result=result.load(), current_time=now.ctime())

@app.route('/riders/add', methods=['GET','POST'])
def radd():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'adddefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        AGE = request.form['age']
        GENDER = request.form['gender']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        YEARS = request.form['years']
        WINS = request.form['wins']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        CHAMP = request.form['champ']
        TOTALP= request.form['totalpoints']
        result.add_default(NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, WINS, PODIUM, POLE, CHAMP, TOTALP)
        return render_template('/riders/add.html', current_time=now.ctime())
    else:
        return render_template('/riders/add.html', current_time=now.ctime())


@app.route('/riders/search', methods=['GET','POST'])
def rsearch():
    now = datetime.datetime.now()
    return render_template('/riders/search.html', current_time=now.ctime())

@app.route('/riders/delete', methods=['GET','POST'])
def rdelete():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'deldefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        result.del_default(NAME, SURNAME)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_by_num(NUM)
    return render_template('/riders/delete.html', current_time=now.ctime())

@app.route('/circuits', methods=['GET', 'POST'])
def circuits_page():
    page = Circuit(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_page()
    elif 'deletecircuitwithid' in request.form:
        id = request.form['id']
        return page.delete_circuit_with_id(id)
    elif 'addcircuit' in request.form:
        name = request.form['name']
        length = request.form['length']
        width = request.form['width']
        left_corners = request.form['left_corners']
        right_corners = request.form['right_corners']
        longest_straight = request.form['longest_straight']
        country = request.form['country']
        constructed_year = request.form['constructed_year']
        return page.add_circuit(name, length, width, left_corners, right_corners, longest_straight, country, constructed_year)

    else:
        return redirect(url_for('home_page'))

class Circuit:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self):
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

            query = "SELECT * FROM circuits"
            cursor.execute(query)
            circuits = cursor.fetchall()
        return render_template('circuits.html', circuits = circuits)
    def delete_circuit_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM circuits WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('circuits_page'))
    def add_circuit(self, name, length, width, left_corners, right_corners, longest_straight, country, constructed_year):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO circuits (name, length, width, left_corners, right_corners, longest_straight, country, constructed_year)
                        VALUES
                        ('%s', %s, %s, %s, %s, %s, '%s', %s)""" % (name, length, width, left_corners, right_corners, longest_straight, country, constructed_year)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('circuits_page'))

@app.route('/brands')
def brands():
    now = datetime.datetime.now()
    return render_template('brands.html', current_time=now.ctime())

@app.route('/seasons')
def seasons():
    now = datetime.datetime.now()
    return render_template('seasons.html', current_time=now.ctime())


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        connection.commit()
    return redirect(url_for('home_page'))


@app.route('/count')
def counter_page():
    now = datetime.datetime.now()
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return render_template('count.html', count = count, current_time=now.ctime())


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
