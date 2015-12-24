Parts Implemented by Nuri Mertcan Guner
=======================================
In this project I implemented parts containing ridersClass, yearstatsClass, personalClass and
fansClass python classes to work with my corresponding SQL tables such as RIDERS, YEARSTATS,
PERSONAL, FANS in the same order.All these classes share some basic operations but working with a
different approach. Below, there are explanations for every operation on these tables.

* Create
* Insert
* Update
* Select
* Delete

General Basic Functions and Explanations
========================================

init Functions
^^^^^^^^^^^^^^
   This function is implemented to create the any table included in this document with all of its
   columns if it does not exist with *CREATE TABLE IF NOT EXISTS* statement in SQL query.

   Example from ridersClass:

.. code-block:: python

    def init(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS RIDERS (
                        NUM serial PRIMARY KEY,
                        NAME text NOT NULL,
                        SURNAME text NOT NULL,
                        AGE integer DEFAULT 0,
                        GENDER text NOT NULL,
                        TEAM text NOT NULL,
                        BRAND text NOT NULL,
                        MODEL text NOT NULL,
                        NATION text NOT NULL,
                        YEARS integer NOT NULL,
                        BIKENO integer UNIQUE
                        )"""    #NUM is index
            cursor.execute(query)
        return




fill Functions
^^^^^^^^^^^^^^
   This function is implemented to insert some default rows to the table its class is created
   for. It inserts every information available and requiured in the table.

   Example from ridersClass:

.. code-block:: python

    def fill(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)
                        VALUES
                        ('Valentino', 'Rossi', 36, 'Male', 'Movistar Yamaha MotoGP', 'Yamaha', 'YZR-M1', 'Italy', 15, 46) ,
                        ('Dani', 'Pedrosa', 30, 'Male','Repsol Honda Team', 'Honda', 'RC213V', 'Spain', 9, 26)"""
            cursor.execute(query)
        return



load_tablename Functions
^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to return every existent tuple with its columns in its table to
   server.py in order to use flusks render_template method to work with html tables which are
   implemented to list SQL table tuples with their columns to the user.

   Example from ridersClass:

.. code-block:: python

    def load_riders(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RIDERS ORDER BY NUM ASC"
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)



Implementation of ridersClass (Riders Table)
============================================
   This class is used to operate on *RIDERS* SQL table and it is implemented in *riders.py* file. This
   SQL table is created to have mandatory information about riders in MotoGP such as their names,
   surnames, team etc. There are also tables including references to this table that is also
   further explained in this document.

Columns of RIDERS
^^^^^^^^^^^^^^^^^
* **NUM :** serial primary key column to distinguish rider row from others
* **NAME :** names of riders as text and can not be NULL
* **SURNAME :** surnames of riders as text and can not be NULL
* **AGE :** ages of riders as an integer and default is 0
* **GENDER :** gender of riders as text and can not be NULL
* **TEAM :** teams of riders as text and can not be NULL
* **BRAND :** bike brands of riders as text and can not be NULL
* **MODEL :** bike models of riders as text and can not be NULL
* **NATION :** nationality of riders as text and can not be NULL
* **YEARS :** years that rider has compete in MotoGP as an integer and cannot be NULL
* **BIKENO :** bike numbers of riders as an integer and a UNIQUE value for each rider

add_rider_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to insert tuples to the *RIDERS* table with *INSERT INTO* SQL query
   statement which gets every columns input from *server.py* (which gets them from related HTML
   forms).


.. code-block:: python

    def add_rider_default(self, name, surname, age, gender, team, brand, model, nation, years, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RIDERS (NAME, SURNAME, AGE, GENDER, TEAM, BRAND, MODEL, NATION, YEARS, BIKENO)    VALUES
                        ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', %s, %s )""" % (name, surname, age, gender, team, brand, model, nation, years, bikeno)
            cursor.execute(query)
            connection.commit()
        return


update_rider_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to update existent tuples with new inputs from *server.py* (which gets them
   from related HTML forms). This function has to get correct inputs even if the user does not want to
   change specific columns of the tuple. *NUM*(primary key) column is used as unique identifier for tuple
   to update the one that user wants and this information is also from *server.py* function call.

.. code-block:: python

    def update_rider_by_num(self, num, name, surname, age, gender, team, brand, model, nation, years, bikeno):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  RIDERS
                        SET NAME = '%s', SURNAME = '%s', AGE = %s, GENDER = '%s', TEAM = '%s', BRAND = '%s', MODEL = '%s', NATION = '%s', YEARS = %s, BIKENO = %s
                        WHERE NUM = '%s' """ % (name, surname, age, gender, team, brand, model, nation, years, bikeno, num)
            cursor.execute(query)
            connection.commit()
        return


search_rider_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to search from existent tuples which includes given inputs in the
   correponding columns of the *RIDERS* table. For implementation with SQL database *SELECT * FROM* query
   statement is used with given inputs from server.py function call. For flexible functionality
   *('%'+stringname+'%')* method is used to get results even if the user did not give the exact information
   in the tuple that is wanted to get as a result.

.. code-block:: python

    def search_rider_default(self, name, surname, team, brand, model, nation):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM RIDERS WHERE NAME LIKE '%s' AND SURNAME LIKE '%s' AND TEAM LIKE '%s'
            AND BRAND LIKE '%s' AND MODEL LIKE '%s' AND NATION LIKE '%s'
            ORDER BY NUM ASC""" % (('%'+name+'%'),('%'+surname+'%'),('%'+team+'%'),('%'+brand+'%'),('%'+model+'%'),('%'+nation+'%'))
            cursor.execute(query)
            riders = cursor.fetchall()
        return (riders)



del_rider_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *RIDERS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *NAME* and *SURNAME* columns in the RIDERS table are
   used to match and delete wanted tuple. This two input information are sent from the *server.py*
   function call.

.. code-block:: python

    def del_rider_default(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NAME = '%s'
                        AND SURNAME = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
        return

del_rider_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *RIDERS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *NUM* column in the RIDERS table is used to match
   and delete wanted tuple. This two input information are sent from the *server.py* function call.Since *NUM*
   column is primary key in the table this function can delete one rider at a time.

.. code-block:: python

    def del_rider_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM RIDERS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return


Implementation of yearstatsClass (Stats Table)
==============================================
   This class is used to operate on *YEARSTATS* SQL table and it is implemented in *stats.py* file. This
   SQL table is created to have mandatory information about riders annually or season statistics in MotoGP such
   as their races completed, victory count, podium count, position at the end of the year etc. This table
   has a foreign key column to the *NUM* column in *RIDERS* table to match riders with their statistics.

Columns of YEARSTATS
^^^^^^^^^^^^^^^^^^^^
* **NUM :** serial primary key column to distinguish statistics row from others
* **YEAR :** year that this row of statistics belongs to, as integer, default is 0
* **RACES :** completed race count that corresponding rider achieved this year, as integer, default is 0
* **VICTORY :** number of times that rider become first in races this year, as integer, default is 0
* **SECOND :** number of times that rider become second in races this year, as integer, default is 0
* **THIRD :** number of times that rider become third in races this year, as integer, default is 0
* **PODIUM :** sum of times that rider become first, second or third in races this year, as integer, default is 0
* **POLE :** number of times that rider got first pole position in race starts this year, as integer, default is 0
* **POINTS :** number of times that rider become first in races this year, as integer, default is 0
* **POSITION :** sum of points that rider got from races completed this year, as integer, default is 0
* **STATID :** foreign key to NUM column in RIDERS table, as serial, has *ON DELETE CASCADE* and *ON UPDATE CASCADE* attributes

add_stats_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to insert tuples to the *YEARSTATS* table with *INSERT INTO* SQL query
   statement which gets every columns input from *server.py* (which gets them from related HTML
   forms). The *statid* input has to match any existent tuple of *RIDERS* tables *NUM* column because it is
   the foreign key in *YEARSTATS* table to match statistics with riders.


.. code-block:: python

    def add_stats_default(self, year, races, victory, second, third, podium, pole, points, position, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO YEARSTATS (YEAR, RACES, VICTORY, SECOND, THIRD, PODIUM, POLE, POINTS, POSITION, STATID)    VALUES
                        ( %s, %s, %s, %s, %s, %s , %s, %s, %s, '%s')""" % (year, races, victory, second, third, podium, pole, points, position, statid)
            cursor.execute(query)
            connection.commit()
        return


update_stats_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to update existent tuples with new inputs from *server.py* (which gets them
   from related HTML forms). This function has to get correct inputs even if the user does not want to
   change specific columns of the tuple. *NUM*(primary key) column is used as unique identifier for tuple
   to update the one that user wants and this information is also from *server.py* function call.
   The *statid* input has to match any existent tuple of *RIDERS* tables *NUM* column because it is
   the foreign key in *YEARSTATS* table to match statistics with riders.

.. code-block:: python

    def update_stats_by_num(self, num, year, races, victory, second, third, podium, pole, points, position, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  YEARSTATS
                        SET YEAR = %s, RACES = %s, VICTORY = %s, SECOND = %s, THIRD = %s, PODIUM = %s, POLE = %s, POINTS = %s, POSITION = %s, STATID = '%s'
                        WHERE NUM = '%s' """ % (year, races, victory, second, third, podium, pole, points, position, statid, num)
            cursor.execute(query)
            connection.commit()
        return


search_stats_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to search from existent tuples which includes given inputs in the
   correponding columns of the *YEARSTATS* table. For implementation with SQL database *SELECT * FROM* query
   statement is used with given inputs from *server.py* function call. For flexible functionality
   four different occasions for this method are considered which results in ability to search even if
   the user leaves *year* or *position* inputs empty or leaves both empty. If they are both left empty
   function returns every tuple in the *YEARSTATS* table. Otherwise it uses *SELECT * FROM* statement for existent
   inputs.

.. code-block:: python

    def search_stats_default(self, year, position):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            if not year and not position:
                query = """SELECT * FROM YEARSTATS ORDER BY NUM ASC"""
            elif not year :
                query = """SELECT * FROM YEARSTATS WHERE POSITION = %s
                    ORDER BY NUM ASC""" % (position)
            elif not position:
                query = """SELECT * FROM YEARSTATS WHERE YEAR = %s ORDER BY NUM ASC""" % (year)
            else:
                query = """SELECT * FROM YEARSTATS WHERE YEAR = %s AND POSITION = %s ORDER BY NUM ASC""" % (year,position)
            cursor.execute(query)
            stats = cursor.fetchall()
        return (stats)


search_stats_by_rider Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to search from existent tuples which includes given inputs in the
   correponding *STATID* column of the *YEARSTATS* table. For implementation with SQL database *SELECT * FROM* query
   statement is used with given inputs from *server.py* function call.

.. code-block:: python

    def search_stats_by_rider(self, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM YEARSTATS WHERE STATID = '%s' ORDER BY NUM ASC""" % (statid)
            cursor.execute(query)
            stats = cursor.fetchall()
        return (stats)



del_stats_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *YEARSTATS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *NUM* column in the *YEARSTATS* table is
   used to match and delete wanted tuple. This input information are sent from the *server.py*
   function call.Since *NUM* column is primary key in the table this function can delete one stat at a time.

.. code-block:: python

    def del_stats_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM YEARSTATS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

del_stats_by_rider Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *YEARSTATS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *STATID* column in the *YEARSTATS* table is
   used to match and delete wanted tuple or tuples as multiple tuples can have the same *STATID* value.
   This input information are sent from the *server.py* function call.

.. code-block:: python

    def del_stats_by_rider(self, statid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM YEARSTATS WHERE STATID = '%s' """ % (statid)
            cursor.execute(query)
            connection.commit()
        return


Implementation of personalClass (Personal Details Table)
========================================================
   This class is used to operate on *PERSONAL* SQL table and it is implemented in *personal.py* file. This
   SQL table is created to have detailed information about riders personalities and social accounts such
   as their birthdays, weights, heights, website links etc. This table has a foreign key column to the *NUM*
   column in *RIDERS* table to match riders with their personal details.

Columns of PERSONAL
^^^^^^^^^^^^^^^^^^^
* **NUM :** serial primary key column to distinguish personal row from others
* **BIRTH :** birthday of the corresponding rider, as date
* **WEIGHT :** calculated weight of the corresponding rider in kg, as integer, default is 0
* **HEIGHT :** calculated height of the corresponding rider in cm, as integer, default is 0
* **FAVCIR :** favorite circuit of the corresponding rider, as text
* **WEBSITE :** link to the official website of the corresponding rider, as text
* **FACEB :** username of the facebook page related to corresponding rider, as text
* **TWIT :** username of the twitter page related to corresponding rider, as text
* **INSTA :** username of the instagram page related to corresponding rider, as text
* **FANS :** sum of fans registered on this website of the correponsing rider, as integer, default is 0
* **PERSID :** foreign key to NUM column in RIDERS table, as serial, has *ON DELETE CASCADE* and *ON UPDATE CASCADE* attributes also has UNIQUE attribute

add_personal_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to insert tuples to the *PERSONAL* table with *INSERT INTO* SQL query
   statement which gets every columns input from *server.py* (which gets them from related HTML
   forms). The *persid* input has to match any existent tuple of *RIDERS* tables *NUM* column because it is
   the foreign key in *PERSONAL* table to match statistics with riders.


.. code-block:: python

    def add_personal_default(self, birth, weight, height, favcir, website, faceb, twit, insta, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PERSONAL (BIRTH, WEIGHT, HEIGHT, FAVCIR, WEBSITE, FACEB, TWIT, INSTA, FANS, PERSID)    VALUES
                        ( '%s', %s, %s, '%s', '%s', '%s' , '%s', '%s', 0, '%s')""" % (birth, weight, height, favcir, website, faceb, twit, insta, persid)
            cursor.execute(query)
            connection.commit()
        return


update_personal_by_rider Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to update existent tuples with new inputs from *server.py* (which gets them
   from related HTML forms). This function has to get correct inputs even if the user does not want to
   change specific columns of the tuple. *PERSID*(unique, foreign key) column is used as unique identifier for tuple
   to update the one that user wants and this information is also from *server.py* function call.
   The *persid* input has to match any existent tuple of *RIDERS* tables *NUM* column because it is
   the foreign key in *PERSONAL* table to match personal details with riders.

.. code-block:: python

    def update_personal_by_rider(self, birth, weight, height, favcir, website, faceb, twit, insta, fans, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  YEARSTATS
                        SET BIRTH = '%s', WEIGHT = %s, HEIGHT = %s, FAVCIR = '%s', WEBSITE = '%s', FACEB = '%s', TWIT = '%s', INSTA = '%s', FANS = %s
                        WHERE PERSID = '%s' """ % (birth, weight, height, favcir, website, faceb, twit, insta, fans, persid)
            cursor.execute(query)
            connection.commit()
        return


search_personal_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to search from existent tuples which includes given *persid* in the
   correponding *PERSID* column of the *PERSONAL* table. For implementation with SQL database *SELECT * FROM* query
   statement is used with given inputs from *server.py* function call. Since *PERSID* column is unique in the
   table this function can search one rider at a time. If input is left blank result would be every tuple
   in the table.

.. code-block:: python

    def search_personal_default(self, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM PERSONAL WHERE PERSID = '%s' ORDER BY FANS DESC""" % (persid)
            cursor.execute(query)
            detail = cursor.fetchall()
        return (detail)



del_personal_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *PERSONAL* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *NUM* column in the *PERSONAL* table is
   used to match and delete wanted tuple. This input information are sent from the *server.py*
   function call.Since *NUM* column is primary key in the table this function can delete one tuple at a time.

.. code-block:: python

    def del_personal_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

del_personal_by_rider Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *PERSONAL* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *PERSID* column in the *PERSONAL* table is
   used to match and delete wanted tuple. This input information are sent from the *server.py*
   function call.Since *PERSID* column is unique foreign key in the table this function can search by one
   rider at a time.

.. code-block:: python

    def del_personal_by_rider(self, persid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE PERSID = '%s' """ % (persid)
            cursor.execute(query)
            connection.commit()
        return


inc_fans Function
^^^^^^^^^^^^^^^^^
   This function has a very basic implementation as it get *num* input and uses *UPDATE .. SET .. WHERE* SQL
   query commands to increase corresponding tuples *FANS* column by one at a time.

.. code-block:: python

       def inc_fans(self, num):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE PERSONAL SET FANS = FANS + 1 WHERE NUM = '%s'" % (num)
            cursor.execute(query)
            connection.commit()
        return


Implementation of fansClass (Rider Fans Table)
==============================================
   This class is used to operate on *FANS* SQL table and it is implemented in *fans.py* file. This
   SQL table is created to have detailed information about riders fans such
   as their names, surnames, birthdays and mail addresses. This table has a foreign key column to the *NUM*
   column in *PERSONAL* table to match personal details with their fans. This is the only table that
   does not have a default fill function because this table is used to store fans registered on
   the website.

Columns of FANS
^^^^^^^^^^^^^^^
* **NUM :** serial primary key column to distinguish fans row from others
* **NAME :** name if the fan registered, as text, can not be NULL
* **SURNAME :** surname of the fan registered, as text, can not be NULL
* **MAIL :** e-mail address of the fan, as text, can not be NULL
* **BIRTH :** birthday of the registered fan, as date
* **FANSID :** foreign key to NUM column in PERSONAL table, as integer, has *ON DELETE CASCADE* and *ON UPDATE CASCADE* attributes


add_fans_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to insert tuples to the *FANS* table with *INSERT INTO* SQL query
   statement which gets every columns input from *server.py* (which gets them from related HTML
   forms). The *fansid* input has to match any existent tuple of *PERSONAL* tables *NUM* column because it is
   the foreign key in *PERSONAL* table to match statistics with riders. This function also uses the
   *UPDATE .. SET .. WHERE* query statements to increase the *FANS* column value for the corresponding tuple.


.. code-block:: python

    def add_fans_default(self, name, surname, mail, birth, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO FANS (NAME, SURNAME, MAIL, BIRTH, FANSID)    VALUES
                        ( '%s', '%s', '%s', '%s', '%s')""" % (name, surname, mail, birth, fansid)
            cursor.execute(query)
            connection.commit()
            cursor = connection.cursor()
            query = "UPDATE PERSONAL SET FANS = FANS + 1 WHERE NUM = '%s'" % (fansid)
            cursor.execute(query)
            connection.commit()
        return


update_fans_by_mail Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to update existent tuples with new inputs from *server.py* (which gets them
   from related HTML forms). This function has to get correct inputs even if the user does not want to
   change specific columns of the tuple. *MAIL* column is used as unique identifier for tuples
   to update the one that user wants and this information is also from *server.py* function call. Although
   this uses current mail address of the fan to update it can also change the mail address to a different one.
   But since this method can be used to update multiple tuple with same *MAIL* column it does not allow to change
   the *FANSID* column to be changed.

.. code-block:: python

    def update_fans_by_mail(self, name, surname, mail, birth, cmail):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  FANS
                        SET NAME = '%s', SURNAME = '%s', MAIL = '%s', BIRTH = '%s'
                        WHERE MAIL LIKE '%s' """ % (name, surname, mail, birth, ('%'+cmail+'%'))
            cursor.execute(query)
            connection.commit()
        return



update_fans_by_mail Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to update existent tuples with new inputs from *server.py* (which gets them
   from related HTML forms). This function has to get correct inputs even if the user does not want to
   change specific columns of the tuple. *NUM*(primary key) column is used as unique identifier for tuples
   to update the one that user wants and this information is also from *server.py* function call.
   The *fansid* input has to match any existent tuple of *PERSONAL* tables *NUM* column because it is
   the foreign key in *FANS* table to match fans with personal details.

.. code-block:: python

    def update_fans_by_num(self, num, name, surname, mail, birth, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE  FANS
                        SET NAME = '%s', SURNAME = '%s', MAIL = '%s', BIRTH = '%s', FANSID = '%s'
                        WHERE NUM = '%s' """ % (name, surname, mail, birth, fansid, num)
            cursor.execute(query)
            connection.commit()
        return


search_fans_default Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to search from existent tuples which includes given inputs in the
   correponding columns of the *FANS* table. For implementation with SQL database *SELECT * FROM* query
   statement is used with given inputs from server.py function call. For flexible functionality
   *('%'+stringname+'%')* method is used to get results even if the user did not give the exact information
   in the tuple that is wanted to get as a result. Also two different occasions are implemented for this method
   one which includes *name*, *surname*, *mail* inputs only and blank for *fansid* input. And the other with
   *fansid* input is not blank, this second occasion also allow us to leave other inputs blank by the help
   of flexible functionality thus can search only by *fansid* with the same query.

.. code-block:: python

    def search_fans_default(self, name, surname, mail, fansid):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            if not fansid :
                query = """SELECT * FROM FANS WHERE NAME LIKE '%s' AND SURNAME LIKE '%s' AND MAIL LIKE '%s'
                ORDER BY NUM ASC""" % (('%'+name+'%'),('%'+surname+'%'),('%'+mail+'%'))
            else:
                query = """SELECT * FROM FANS WHERE NAME LIKE '%s' AND SURNAME LIKE '%s' AND MAIL LIKE '%s' AND FANSID = '%s'
                ORDER BY NUM ASC""" % (('%'+name+'%'),('%'+surname+'%'),('%'+mail+'%'),fansid)
            cursor.execute(query)
            fans = cursor.fetchall()
        return (fans))



del_fans_by_num Function
^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *FANS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *NUM* column in the *FANS* table is
   used to match and delete wanted tuple. This input information are sent from the *server.py*
   function call.Since *NUM* column is primary key in the table this function can delete one tuple at a time.

.. code-block:: python

    def del_fans_by_num(self, num):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FANS WHERE NUM = '%s' """ % (num)
            cursor.execute(query)
            connection.commit()
        return

del_fans_by_mail Function
^^^^^^^^^^^^^^^^^^^^^^^^^
   This function is implemented to delete specific tuples from the *FANS* table using the *DELETE FROM* and
   *WHERE* SQL query statements. In this delete operation *MAIL* column in the *FANS* table is
   used to match and delete wanted tuple. This input information are sent from the *server.py*
   function call.Since *MAIL* can be existent multiple times on different tuples thus, this method allows user
   to delete multiple tuple at a time.

.. code-block:: python

    def del_fans_by_mail(self, mail):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PERSONAL WHERE MAIL = '%s' """ % (mail)
            cursor.execute(query)
            connection.commit()
        return




