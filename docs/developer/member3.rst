Parts Implemented by Göktuğ Öcalan
==================================

Parts implemented by me are the teams, countries and standings classes and tables. Their operations, html and css files are also implemented by me.

Tables
------

1.Teams
,,,,,,,
The table has the following attributes:

- **id:** Automatically generated ID. Type is serial. It is the primary key of the table.
- **name:** Name of the team. Type is text. It has the quality unique.
- **country:** Origin country of the team. Type is text. It references the "abbreviation" attribute of the countries table. It is restricted for delete and cascaded for update operations.
- **constructor:** Motorycycle supplying brand for the team. Type is text. It can't be null.
- **motorcycle:** Model of the supplied motorcycle. Type is text. It can't be null.
- **riderNo:** Number of riders the team has. Type is integer. It defaults to 0.

2.Countries
,,,,,,,,,,,
The table has the following attributes:

- **name:** Name of the country. Type is text. It can't be null.
- **abbreviation:** 3 letter abbreviation of the country defined by ISO. Type is text. It is the primary key of the table. It can't be null.
- **continent:** Continent the country belongs to. Type is text. It can't be null.

3.Standings
,,,,,,,,,,,
The table has the following attributes:

- **position:** Teams position in the standings table. Type is integer. It is the primary key of the table.
- **name:** Name of the team. Type is text. It references the "name" attribute of the teams table. It is cascaded for both update and delete.
- **points:** Number of points the team has. Type is integer. It defaults to 0.

Server.py
---------

My contribution in the server.py file can be divided into 3 very similar parts. Each part handles the requests for a different class and table. An object of the desired class is created and the given parameters are passed to intended functions. The following part is the code from the teams part::

   @app.route('/teams', methods=['GET', 'POST'])
   def teamsPage():
       page = Teams(dsn = app.config['dsn'])
       if request.method == 'GET':
           page.createTable();
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
       elif 'searchTeam' in request.form:
           name = request.form['name']
           country = request.form['country']
           constructor = request.form['constructor']
           motorcycle = request.form['motorcycle']
           return page.searchTeam(name, country, constructor, motorcycle)

All Class Functions
-------------------

Functions in this segment are identical in all classes.

createTable:
,,,,,,,,,,,,

This function creates all 3 tables if they don't already exist::

    def createTable(self):      #this create all 3 tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS countries (
                        name text NOT NULL,
                        abbreviation text NOT NULL PRIMARY KEY,
                        continent text NOT NULL)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS teams (
                        id serial PRIMARY KEY,
                        name text UNIQUE,
                        country text REFERENCES countries(abbreviation) ON DELETE RESTRICT ON UPDATE CASCADE,
                        constructor text NOT NULL,
                        motorcycle text NOT NULL,
                        riderNo integer DEFAULT 0)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS standings (
                        position integer PRIMARY KEY,
                        name text UNIQUE REFERENCES teams(name) ON UPDATE CASCADE ON DELETE CASCADE,
                        points integer DEFAULT 0)"""
            cursor.execute(query)

dropTable:
,,,,,,,,,,

This function drops all 3 tables::

    def dropTable(self):        #This drops all three tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS countries CASCADE"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS teams CASCADE"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS standings"""
            cursor.execute(query)

            connection.commit()

initTable:
,,,,,,,,,,

This function first drops the tables and then creates them by calling the previously explained functions. After that it inserts predetermined values to all three tables::

    def initTable(self):        #this initializes all 3 tables
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            self.dropTable()
            self.createTable()

            query = """INSERT INTO countries (name, abbreviation, continent)
                        VALUES
                        ('ITALY', 'ITA', 'EUROPE'),
                        ('JAPAN', 'JPN', 'ASIA'),
                        ('CZECH REPUBLIC', 'CZE', 'EUROPE'),
                        ('AUSTRALIA', 'AUS', 'AUSTRALIA'),
                        ('SWITZERLAND', 'CHE', 'EUROPE'),
                        ('FRANCE', 'FRA', 'EUROPE'),
                        ('UNITED STATES OF AMERICA', 'USA', 'NORTH AMERICA'),
                        ('SPAIN', 'ESP', 'EUROPE'),
                        ('COLOMBIA', 'COL', 'SOUTH AMERICA')"""
            cursor.execute(query)

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('REPSOL HONDA TEAM', 'JPN', 'HONDA', 'RC213V', 3),
                        ('DUCATI TEAM', 'ITA', 'DUCATI', 'DESMOSEDICI GP15', 3),
                        ('AB MOTORACING', 'CZE', 'HONDA', 'RC213V-RS', 5),
                        ('MOVISTAR YAMAHA MOTOGP', 'JPN', 'YAMAHA', 'YZR-M1', 2),
                        ('ATHINA FORWARD RACING', 'CHE', 'YAMAHA', 'FORWARD', 4),
                        ('APRILIA RACING TEAM GRESINI', 'ITA', 'APRILIA', 'RS-GP', 4),
                        ('MONSTER YAMAHA TECH 3', 'FRA', 'YAMAHA', 'YZR-M1', 2)"""
            cursor.execute(query)

            query = """INSERT INTO standings (position, name, points)
                        VALUES
                        (2, 'REPSOL HONDA TEAM', 453),
                        (3, 'DUCATI TEAM', 350),
                        (14, 'AB MOTORACING', 0),
                        (1, 'MOVISTAR YAMAHA MOTOGP', 655),
                        (10, 'ATHINA FORWARD RACING', 39),
                        (11, 'APRILIA RACING TEAM GRESINI', 39),
                        (4, 'MONSTER YAMAHA TECH 3', 295)"""
            cursor.execute(query)

            connection.commit()

Class Specific Functions
------------------------
Functions in this section are similar but have small differences based on the attributes of the table they belong to. Also every function that returns some information for the html code also returns the current time so the navigation bar can use it.

loadPage:
,,,,,,,,,

This function is called every time the specific url for the class is requested. It either selects the entire database or it performs a filtered select on the database based on class variables that are altered via the search function. After being called once it resets the variables back to an empty string. It returns the resulting relation to the html code::

    def loadPage(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM teams WHERE name LIKE '%s'
            AND country LIKE '%s' AND constructor LIKE '%s'
            AND motorcycle LIKE '%s' ORDER BY id ASC""" % (('%' + Teams.searchName + '%'),
            ('%' + Teams.searchCountry + '%'),('%' + Teams.searchConstructor + '%'),
            ('%' + Teams.searchMotorcycle + '%'))

            Teams.searchName = ''
            Teams.searchCountry = ''
            Teams.searchConstructor = ''
            Teams.searchMotorcycle = ''

            cursor.execute(query)

            teamsdb = cursor.fetchall()
            now = datetime.datetime.now()
        return render_template('teams.html', teams = teamsdb, current_time=now.ctime())

addClassName:
,,,,,,,,,,,,,

**The name for this function is a placeholder. The actual functions in the code are "addTeam", "addCountry" and "addstanding".**

This function is called when the corresponding addClassName form is sent from the html code. It is called from server.py and the information in the html form are passed as parameters. It inserts a new tuple to the table with the given attributes. All text are converted to uppercase. At the end, the page url is redirected to itself so it basically refreshes the page so the new values can be showed to the user::

    def addTeam(self, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO teams (name, country, constructor, motorcycle, riderNo)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s)""" % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

updateClassName:
,,,,,,,,,,,,,,,,

**The name for this function is a placeholder. The actual functions in the code are "updateTeam", "updateCountry" and "updatestanding".**

This function is called when the corresponding updateClassName form is sent from the html code. The information in the form is passed through server.py as parameters for this function. All existing tuples that matches the parameters are updated with new attributes. Page is also refreshed again::

    def updateTeam(self, id, name, country, constructor, motorcycle, riderNo):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE teams
                        SET name = '%s', country = '%s', constructor = '%s', motorcycle = '%s', riderNo = %s
                        WHERE id = '%s' """ % (name.upper(), country.upper(), constructor.upper(), motorcycle.upper(), riderNo, id)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('teamsPage'))

deleteClassName:
,,,,,,,,,,,,,,,,

**The name for this function is a placeholder. The actual functions in the code are "deleteTeamId", "deleteCountry" and "deletestanding".**

This function is called when the corresponding deleteClassName form is sent from the html code. Every tuple that matches the selected attribute are deleted. Page is also refreshed again::

    def deleteTeamId(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM teams WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('teamsPage'))

searchClassName:
,,,,,,,,,,,,,,,,

**The name for this function is a placeholder. The actual functions in the code are "searchTeam", "searchCountry" and "searchstanding".**

This function is called when the corresponding searchClassName form is sent from the html code. Given paramters are stored as a class variable. The page is refreshed which calls the loadPage function. Stored variables are used to select the intended part of the database by sending a select query. Variables are resetted to empty strings after the first loadPage so when the page is loaded again next time, the full database is listed. This logic works because every attribute in every tuple technically includes an empty string::

    def searchTeam(self, name, country, constructor, motorcycle):
        Teams.searchName = name.upper()
        Teams.searchCountry = country.upper()
        Teams.searchConstructor = constructor.upper()
        Teams.searchMotorcycle = motorcycle.upper()
        return redirect(url_for('teamsPage'))
