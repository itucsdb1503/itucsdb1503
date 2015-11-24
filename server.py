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
from stats import yearstatsClass
from teams import Teams
from countries import Countries
from circuits import Circuit
from races import Race
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
    elif 'initTable' in request.form:
        return page.initTable()
    elif 'updateTeam' in request.form:
        id = request.form['id']
        name = request.form['name']
        country = request.form['country']
        constructor = request.form['constructor']
        motorcycle = request.form['motorcycle']
        riderNo = request.form['riderNo']
        return page.updateTeam(id, name, country, constructor, motorcycle, riderNo)
    elif 'deleteTeam' in request.form:
        id = request.form['id']
        return page.deleteTeamId(id)
    elif 'searchTeamName' in request.form:
        name = request.form['name']
        return page.searchTeamName(name)

@app.route('/countries', methods=['GET', 'POST'])
def countriesPage():
    page = Countries(dsn = app.config['dsn'])
    if request.method == 'GET':
        page.createTable();
        #page.insertTestTuples();
        return page.loadPage()
    elif 'addCountry' in request.form:
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        continent = request.form['continent']
        return page.addCountry(name, abbreviation, continent)
    elif 'initTable' in request.form:
        return page.initTable()
    elif 'updateCountry' in request.form:
        name = request.form['name']
        newName = request.form['newName']
        abbreviation = request.form['abbreviation']
        continent = request.form['continent']
        return page.updateCountry(name, newName, abbreviation, continent)
    elif 'deleteCountry' in request.form:
        name = request.form['name']
        return page.deleteCountryName(name)
    elif 'searchCountryName' in request.form:
        name = request.form['name']
        return page.searchCountryName(name)

@app.route('/rsreset', methods=['GET','POST'])
def rsreset():
    with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS YEARSTATS"""
            cursor.execute(query)
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS RIDERS"""
            cursor.execute(query)
            cursor = connection.cursor()
            query = """DROP TABLE IF EXISTS STATS"""
            cursor.execute(query)
    riders = ridersClass(dsn = app.config['dsn'])
    riders.fill()
    stats = yearstatsClass(dsn = app.config['dsn'])
    stats.fill()
    return redirect(url_for('home_page'))

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
        BIKENO = request.form['bikeno']
        result.add_rider_default(NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
    elif 'updatebynum' in request.form:
        NUM = request.form['num']
        NAME = request.form['name']
        SURNAME = request.form['surname']
        AGE = request.form['age']
        GENDER = request.form['gender']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        YEARS = request.form['years']
        BIKENO = request.form['bikeno']
        result.update_rider_by_num(NUM, NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
    elif 'searchdefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        return render_template('/riders.html', result=result.search_rider_default(NAME,SURNAME, TEAM, BRAND, MODEL, NATION), current_time=now.ctime())
    elif 'deldefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        result.del_rider_default(NAME, SURNAME)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_rider_by_num(NUM)
    return render_template('/riders.html', result=result.load_riders(), current_time=now.ctime())

@app.route('/riders/list', methods=['GET','POST'])
def rlist():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    return render_template('/riders/list.html', result=result.load_riders(), current_time=now.ctime())

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
        BIKENO = request.form['bikeno']
        result.add_rider_default(NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
    return render_template('/riders/add.html', result=result.load_riders(), current_time=now.ctime())

@app.route('/riders/search', methods=['GET','POST'])
def rsearch():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'searchdefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        return render_template('/riders/search.html', result=result.search_rider_default(NAME,SURNAME, TEAM, BRAND, MODEL, NATION), current_time=now.ctime())
    elif request.method == 'GET':
        return render_template('/riders/search.html', result=result.load_riders(), current_time=now.ctime())
    return render_template('/riders/search.html', result=result.load_riders(), current_time=now.ctime())

@app.route('/riders/update', methods=['GET','POST'])
def rupdate():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'updatebynum' in request.form:
        NUM = request.form['num']
        NAME = request.form['name']
        SURNAME = request.form['surname']
        AGE = request.form['age']
        GENDER = request.form['gender']
        TEAM = request.form['team']
        BRAND = request.form['brand']
        MODEL = request.form['model']
        NATION = request.form['nation']
        YEARS = request.form['years']
        BIKENO = request.form['bikeno']
        result.update_rider_by_num(NUM, NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
    return render_template('/riders/update.html', result=result.load_riders(), current_time=now.ctime())

@app.route('/riders/delete', methods=['GET','POST'])
def rdelete():
    result = ridersClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'deldefault' in request.form:
        NAME = request.form['name']
        SURNAME = request.form['surname']
        result.del_rider_default(NAME, SURNAME)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_rider_by_num(NUM)
    return render_template('/riders/delete.html', result=result.load_riders(), current_time=now.ctime())

@app.route('/riders/stats', methods=['GET','POST'])
def stats():
    riders = ridersClass(dsn = app.config['dsn'])
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'adddefault' in request.form:
        YEAR = request.form['year']
        RACES = request.form['races']
        VICTORY = request.form['victory']
        SECOND = request.form['second']
        THIRD = request.form['third']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        POINTS = request.form['points']
        POSITION= request.form['position']
        STATID = request.form['statid']
        result.add_stats_default(YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)
    elif 'updatebynum' in request.form:
        NUM = request.form['num']
        YEAR = request.form['year']
        RACES = request.form['races']
        VICTORY = request.form['victory']
        SECOND = request.form['second']
        THIRD = request.form['third']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        POINTS = request.form['points']
        POSITION= request.form['position']
        STATID = request.form['statid']
        result.update_stats_by_num(NUM, YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)
    elif 'searchdefault' in request.form:
        YEAR = request.form['year']
        POSITION = request.form['position']
        return render_template('/riders/stats.html', result=result.search_stats_default(YEAR, POSITION), riders=riders.load_riders(), current_time=now.ctime())
    elif 'searchbyrider' in request.form:
        STATID = request.form['statid']
        return render_template('/riders/stats.html', result=result.search_stats_by_rider(STATID),riders=riders.load_riders(), current_time=now.ctime())
    elif 'delbyrider' in request.form:
        STATID = request.form['statid']
        result.del_stats_by_rider(STATID)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_stats_by_num(NUM)
    return render_template('/riders/stats.html', result=result.load_stats(),riders=riders.load_riders(), current_time=now.ctime())

@app.route('/riders/stats/list', methods=['GET','POST'])
def slist():
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    return render_template('/riders/stats/list.html', result=result.load_stats(), current_time=now.ctime())

@app.route('/riders/stats/add', methods=['GET','POST'])
def sadd():
    riders = ridersClass(dsn = app.config['dsn'])
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'adddefault' in request.form:
        YEAR = request.form['year']
        RACES = request.form['races']
        VICTORY = request.form['victory']
        SECOND = request.form['second']
        THIRD = request.form['third']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        POINTS = request.form['points']
        POSITION= request.form['position']
        STATID = request.form['statid']
        result.add_stats_default(YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)
    return render_template('/riders/stats/add.html', result=result.load_stats(),riders=riders.load_riders(), current_time=now.ctime())

@app.route('/riders/stats/search', methods=['GET','POST'])
def ssearch():
    riders = ridersClass(dsn = app.config['dsn'])
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'searchdefault' in request.form:
        YEAR = request.form['year']
        POSITION = request.form['position']
        return render_template('/riders/stats/search.html', result=result.search_stats_default(YEAR, POSITION),riders=riders.load_riders(), current_time=now.ctime())
    elif 'searchbyrider' in request.form:
        STATID = request.form['statid']
        return render_template('/riders/stats/search.html', result=result.search_stats_by_rider(STATID),riders=riders.load_riders(), current_time=now.ctime())
    return render_template('/riders/stats/search.html', result=result.load_stats(),riders=riders.load_riders(), current_time=now.ctime())

@app.route('/riders/stats/update', methods=['GET','POST'])
def supdate():
    riders = ridersClass(dsn = app.config['dsn'])
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'updatebynum' in request.form:
        NUM = request.form['num']
        YEAR = request.form['year']
        RACES = request.form['races']
        VICTORY = request.form['victory']
        SECOND = request.form['second']
        THIRD = request.form['third']
        PODIUM = request.form['podium']
        POLE = request.form['pole']
        POINTS = request.form['points']
        POSITION= request.form['position']
        STATID = request.form['statid']
        result.update_stats_by_num(NUM, YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)
    return render_template('/riders/stats/update.html', result=result.load_stats(),riders=riders.load_riders(), current_time=now.ctime())

@app.route('/riders/stats/delete', methods=['GET','POST'])
def sdelete():
    riders = ridersClass(dsn = app.config['dsn'])
    result = yearstatsClass(dsn = app.config['dsn'])
    now = datetime.datetime.now()
    if 'delbyrider' in request.form:
        STATID = request.form['statid']
        result.del_stats_by_rider(STATID)
    elif 'delbynum' in request.form:
        NUM = request.form['num']
        result.del_stats_by_num(NUM)
    return render_template('/riders/stats/delete.html', result=result.load_stats(),riders=riders.load_riders(), current_time=now.ctime())

@app.route('/circuits', methods=['GET', 'POST'])
def circuits_page():
    page = Circuit(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.list_page()
    elif 'deletecircuitwithid' in request.form:
        id = request.form['id']
        return page.delete_circuit_with_id(id)
    elif 'updatecircuit' in request.form:
        id = request.form['id']
        name = request.form['name']
        length = request.form['length']
        width = request.form['width']
        left_corners = request.form['left_corners']
        right_corners = request.form['right_corners']
        longest_straight = request.form['longest_straight']
        country = request.form['country']
        constructed_year = request.form['constructed_year']
        return page.update_circuit(name, length, width, left_corners, right_corners, longest_straight, country, constructed_year, id)
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
    elif 'searchcircuit' in request.form:
        page.search_name = request.form['name']
        return page.search_circuit(page.search_name)
    else:
        return redirect(url_for('home_page'))

@app.route('/races', methods=['GET', 'POST'])
def races_page():
    page = Race(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.list_page()
    elif 'deleteracewithid' in request.form:
        id = request.form['id']
        return page.delete_race_with_id(id)
    elif 'updaterace' in request.form:
        id = request.form['id']
        name = request.form['name']
        fastest_lap_time = request.form['fastest_lap_time']
        winners_average_lap_time = request.form['winners_average_lap_time']
        average_lap_time = request.form['average_lap_time']
        first_position = request.form['first_position']
        track_circuit_id = request.form['track_circuit_id']
        number_of_laps = request.form['number_of_laps']
        total_accidents = request.form['total_accidents']
        return page.update_race(name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id, number_of_laps, total_accidents, id)
    elif 'addrace' in request.form:
        name = request.form['name']
        fastest_lap_time = request.form['fastest_lap_time']
        winners_average_lap_time = request.form['winners_average_lap_time']
        average_lap_time = request.form['average_lap_time']
        first_position = request.form['first_position']
        track_circuit_id = request.form['track_circuit_id']
        number_of_laps = request.form['number_of_laps']
        total_accidents = request.form['total_accidents']
        return page.add_race(name, fastest_lap_time, winners_average_lap_time, average_lap_time, first_position, track_circuit_id, number_of_laps,total_accidents)
    elif 'searchrace' in request.form:
        page.search_name = request.form['name']
        return page.search_race(page.search_name)
    else:
        return redirect(url_for('home_page'))



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
