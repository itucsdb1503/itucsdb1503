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
        page.insertTestTuples();
        return page.openPage()

    now = datetime.datetime.now()
    return render_template('teams.html', current_time=now.ctime())

@app.route('/riders')
def riders():
    now = datetime.datetime.now()
    return render_template('riders.html', current_time=now.ctime())

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


@app.route('/riders/search')
def rsearch():
    now = datetime.datetime.now()
    return render_template('/riders/search.html', current_time=now.ctime())

@app.route('/riders/delete')
def rdelete():
    now = datetime.datetime.now()
    return render_template('/riders/delete.html', current_time=now.ctime())

@app.route('/circuits')
def circuits():
    now = datetime.datetime.now()
    return render_template('circuits.html', current_time=now.ctime())

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
