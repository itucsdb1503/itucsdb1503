Parts Implemented by Hatice Ozdemir
===================================
In here, there are some technical details about Python, HTML and
CSS codes for Brands, Models and Specifications (models in detail) tables.

Python
------
The technologies that are used with Python (version 3.4) programming language are Flask for web
framework, Psycopg2 for connection between Python and PostgreSQL database and Sphinx for documentation.
Each table has its own python file. For example, Brands table has brands.py file that includes
Python codes for operations and initializations and it is connected with server.

Server
,,,,,,
In server, datetime, json, os, psycopg2 as dbapi2, re are imported. From flask request, render_template,
import url_for and redirect operations are imported. Finally each class for tables is imported from their
python file. With @app.route, URL and HTML methods and functions are defined. Each functions connect HTML requests
and tables' python files. Here is example code from server that defines Brands.

.. code-block:: python

   @app.route('/brands', methods=['GET', 'POST'])
   def brandsPage():
    page = Brand(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.list()

    elif 'addBrand' in request.form:
        name = request.form['name']
        country = request.form['country']
        year = request.form['year']
        champion = request.form['champion']
        return page.addBrand(name, country, year, champion)
    elif 'dbynameBrand' in request.form:
        name = request.form['name']
        return page.deletebyName(name)
    elif 'dbyidBrand' in request.form:
        ID = request.form['ID']
        return page.deletebyId(ID)
    elif 'updateBrand' in request.form:
        ID = request.form['ID']
        name = request.form['name']
        country = request.form['country']
        year = request.form['year']
        champion = request.form['champion']
        return page.update(ID, name, country, year, champion)
    elif 'deleteAllBrands' in request.form:
        return page.deleteAll()
    elif 'AutoFillBrands' in request.form:
        return page.autoFill()
    elif 'searchbyName' in request.form:
        name = request.form['name']
        return page.find(name)
    else:
        return redirect(url_for('home_page'))

Brands
,,,,,,
Class Brand is defined in brands.py file and all its operations are initialized there.

Table
+++++
Brands table has got the columns;

* ID
* name
* country
* year
* champion

.. note::
   Note : Detailed explanations of columns are given in User Guide.

It is initialized as;

.. code-block:: python

   """CREATE TABLE IF NOT EXISTS brands (
                        ID serial PRIMARY KEY,
                        name text NOT NULL UNIQUE,
                        country text NOT NULL,
                        year integer DEFAULT 0,
                        champion integer DEFAULT 0)"""

ID is the primary key.

Operations
++++++++++
Operations of Brands table are;

* list
* addBrand
* deletebyName
* deletebyId
* update
* deleteAll
* autoFill
* find

**list:** This function creates table if it does not exists, selects all elements of table and returns table's
html page.

**addBrand:** This function adds new rows to the table with name, country, year, champion variables
that is came from server accordingly html entry. Name and country must be text, year and champion must be integer
to avoid possible errors.

**deletebyName:** This function deletes rows from table with name variable that is taken input of the user.

**deletebyId:** This function deletes rows from table with ID variable that is taken input of the user.

**update:** This function updates rows of the table which is selected by user with its ID. User must enter all of
the columns even if he/she wants to change only one feature so its variables are  ID, name, country, year, champion.
Name and country must be text, ID, year and champion must be integer to avoid possible errors.

**deleteAll:** This function drops the table if it exists.

**autoFill:** This function automatically fills rows of the table with predetermined, real values.

**find:** This function searches brands by name. So its variable is name with text format. It returns selected part
of table. It is independent and case sensitive. For example, if someone is trying to search 'li', function returns
both 'Ali' and 'Veli'.

Here are codes of addBrand and deleteAll operations;

.. code-block:: python

   def addBrand(self, name, country, year, champion):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO brands (name, country, year, champion)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (name, country, year, champion)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))

.. code-block:: python

   def deleteAll(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS brands CASCADE"""
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('brandsPage'))



Models
,,,,,,
Class Model is defined in models.py file and all its operations are initialized there.
Table
+++++
Models table has got the columns;

* ID
* name
* rider
* constructor

.. note::
   Note : Detailed explanations of columns are given in User Guide.

It is initialized as;

.. code-block:: python

   """CREATE TABLE IF NOT EXISTS models (
                        ID serial PRIMARY KEY,
                        name text NOT NULL,
                        rider text NOT NULL,
                        constructor text REFERENCES brands(name) ON DELETE CASCADE ON UPDATE CASCADE)"""

ID is the primary key and constructor references name in brands table. It is not restricted. It has cascade on
delete and update.

Operations
++++++++++
Operations of Models table are;

* list
* addBrand
* deletebyName
* deletebyId
* update
* deleteAll
* autoFill
* find

**list:** This function creates table if it does not exists, selects all elements of table and returns table's
html page.

**addBrand:** This function adds new rows to the table with name, rider, constructor variables
that is came from server accordingly html entry. All these variables must be in text format
to avoid possible errors.

**deletebyName:** This function deletes rows from table with name variable that is taken input of the user.

**deletebyId:** This function deletes rows from table with ID variable that is taken input of the user.

**update:** This function updates rows of the table which is selected by user with its ID. User must enter all of
the columns even if he/she wants to change only one feature so its variables are  ID, name, rider, constructor.
name, rider, constructor must be text, ID must be integer to avoid possible errors.

**deleteAll:** This function drops the table if it exists.

**autoFill:** This function automatically fills rows of the table with predetermined, real values. These values are
also compatible with foreign key.

**find:** This function searches models by name. So its variable is name with text format. It returns selected part
of table. It is independent and case sensitive.

Here are codes of deletebyName and find operations;

.. code-block:: python

   def deletebyName(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM models WHERE name = '%s' " % (name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('modelsPage'))

.. code-block:: python

   def find(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM models WHERE name LIKE '%s'""" % ('%'+name+'%')
            cursor.execute(query)

            modelsdb = cursor.fetchall()
        return render_template('models.html', models = modelsdb)


Specifications
,,,,,,,,,,,,,,
Class Specification is defined in specifications.py file and all its operations are initialized there.
Table
+++++
Specifications table has got the columns;

* ID
* model
* engine
* fuel
* power
* speed
* weight

.. note::
   Note : Detailed explanations of columns are given in User Guide.

It is initialized as;

.. code-block:: python

   """CREATE TABLE IF NOT EXISTS specifications (
                        ID serial PRIMARY KEY,
                        model text NOT NULL UNIQUE,
                        engine text NOT NULL,
                        fuel integer DEFAULT 0,
                        power integer DEFAULT 0,
                        speed integer DEFAULT 0,
                        weight integer DEFAULT 0)"""

ID is the primary key. This table is independent.

Operations
++++++++++
Operations of Specifications table are;

* list
* addBrand
* deletebyName
* deletebyId
* update
* deleteAll
* autoFill
* find

**list:** This function creates table if it does not exists, selects all elements of table and returns table's
html page.

**addBrand:** This function adds new rows to the table with model, engine, fuel, power, speed, weight variables
that is came from server accordingly html entry. model, engine must be in text format and fuel, power, speed, weight
must be integer to avoid possible errors.

**deletebyName:** This function deletes rows from table with model variable that is taken input of the user.

**deletebyId:** This function deletes rows from table with ID variable that is taken input of the user.

**update:** This function updates rows of the table which is selected by user with its ID. User must enter all of
the columns even if he/she wants to change only one feature so its variables are  ID, model, engine, fuel, power, speed,
weight. model, engine must be in text format and ID, fuel, power, speed, weight must be integer to avoid possible errors.

**deleteAll:** This function drops the table if it exists.

**autoFill:** This function automatically fills rows of the table with predetermined, real values.

**find:** This function searches models by model. So its variable is model with text format. It returns selected part
of table. It is independent and case sensitive.

Here are codes of update and autoFill operations;

.. code-block:: python

   def deletebyName(self, name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM models WHERE name = '%s' " % (name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('modelsPage'))

.. code-block:: python

   def autoFill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS specifications CASCADE"""
            cursor.execute(query)

            query1 = """CREATE TABLE IF NOT EXISTS specifications (
                        ID serial PRIMARY KEY,
                        model text NOT NULL UNIQUE,
                        engine text NOT NULL,
                        fuel integer DEFAULT 0,
                        power integer DEFAULT 0,
                        speed integer DEFAULT 0,
                        weight integer DEFAULT 0)"""
            cursor.execute(query1)

            query2 = """INSERT INTO specifications (model, engine, fuel, power, speed, weight)
                        VALUES
                        ('YZR-M1', '1,000 cc, Inline-4', 21, 183, 340, 157),
                        ('RC213V', '1,000 cc, four-stroke', 21, 176, 350, 160),
                        ('GP15', '1,000 cc, four-stroke', 21, 179, 340, 158),
                        ('GSX-RR', 'Japan', 24, 169, 330, 160)"""
            cursor.execute(query2)
            connection.commit()
        return redirect(url_for('specificationsPage'))

HTML
----
HTML is used to design the project as template. GET and POST methods are used. HTML files takes variables from database
with a for loop and uses them in its methods. '/brands', '/models', '/models/specifications' are URL for brands, models
and specifications tables. All three table has its own HTML file but they are similar. Brands table has brands.html,
models table has models.html and specifications table has specifications.html files.

Here are some examples of HTML codes;

* This code is for listing table

.. code-block:: python

   <table class="brands">
        <tr>
         <td class="brands"> ID </td>
         <td class="brands"> Name </td>
         <td class="brands"> Country </td>
         <td class="brands"> Foundation Year </td>
         <td class="brands"> #Constructor Championship </td>
        </tr>
         {% for ID, name, country, year, champion in brands %}
         <tr>
            <td class="brands"> {{ID}} </td>
            <td class="brands"> {{name}} </td>
            <td class="brands"> {{country}} </td>
            <td class="brands"> {{year}} </td>
            <td class="brands"> {{champion}} </td>
         </tr>
         {%endfor%}
    </table>

* This code is for find operation

.. code-block:: python

   <form id="searchbyName" class= "klas" action="{{ url_for('brandsPage') }}" method="post">
      <table align="center" ,style="width:25%">
            <th class= "klas">Name: </th>
            <td>
               <input type="text" name="name"/>
            </td>
            <td>
               <input value="Find Brand" name="searchbyName" type="submit"/>
            </td>
      </table>
    </form>

CSS
---
CSS is used to design the project with HTML. All three tables use same CSS file which is named as brands.css

Here are some examples of CSS codes;

.. code-block:: python

   h1{
   text-align: center;
   color: #990066 ;
   }
   table.brands{
   text-align: center;
   width: 80%;
   margin-left:auto;
    margin-right:auto;
   color: #F0F0F0 ;
   }
   table.models{
   text-align: center;
   width: 80%;
   margin-left:auto;
    margin-right:auto;
   color: #F0F0F0 ;
   }
   table.specifications{
   text-align: center;
   width: 80%;
   margin-left:auto;
    margin-right:auto;
   color: #F0F0F0 ;
   }
   form.klas{
   color: #A80000;
   }



