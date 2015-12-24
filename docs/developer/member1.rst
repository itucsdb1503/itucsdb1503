Parts Implemented by Mehmet Emir Memmi
======================================
    As my part of the project I implemented circuits,races and accidents and functions related to those tables. I created related classes as python documents and listed functons and their use are given below.

Circuit Class Table Contents
----------------------------
* **id:** primary key of the table as serial type
* **name:** represents the name of the circuit as text which can not be NULL
* **length:** keeps the length information of the circuit as integer which is 0 by default
* **width:** keeps the width information of the circuit as integer which is 0 by default
* **left_corners:** keeps the left corner count information of the circuit as integer which is 0 by default
* **right_corners:** keeps the right corner count information of the circuit as integer which is 0 by default
* **longest_straight:** keeps the longest straight information  as meter which is integer with default value as 0
* **country:** keeps the country that the circuit is in which is text and can not be NULL
* **constructed_year:** keeps the year of construction of the circuit as integer variable which has 0 as default value

Note About The Table:
,,,,,,,,,,,,,,,,,,,,,
   At the start of my circuits_page() function in server.py, related Circuit class object is being created. The related if clauses' function calls are being held by this instantiated
   object later on as return statements.

Circuit Class Methods' Implementations
--------------------------------------
Search Method Implementation:
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   Global variable search_bool which is 0 by default is being kept as the identifier for my if conditions. search_name which is empty text is also kept for storing
   the intended text for searching. As the user enters the text of interest in the search area and presses the search button at my circuit.html interface the function
   circits_page() is being called from server.py document. It enters the 'searchcircuit' if condtional and gets the data from html document and runs the search_circuit function
   of my Circuit class. My search_circuit function takes self and name as an arguement and changes search_bool to 1 and changes the entered text to upper for case insensitive search.

   My function redirects to my circuits_page as a return operation. From here my list_page() function is being used for printing the intended search variable. I implemented an if conditional that looks
   if search_bool is 1. If so it selects the rows where the intended search text is present in any location of the name column of circuits table. It is being done by using LIKE and '%' commands as prefix and postfix
   of the search_name variable. If there are multiple outputs, outputs are being printed in ascending order.

Delete Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   My delete function works as the user enters the id of the unwanted row and presses the delete button in my html form. As soon as the user does that my circuits_page() function in server.py is being called by my html form and it
   enters the 'deletecircuitwithid' if conditional. From there it sends the id variable to my delete_circuit_with_id function which is in my Circuit class. In delete_circuit_with_id(self,id) function a connection to circuits table is being created
   and deletion operation is being done by delete query of sql language where the id is equal to the input which is entered by the user. Then redirection to the circuits_page is being done by return statement of the function.

Add Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,
   As soon as the user fills all the related row information on the html page and presses the 'Add Circuit' button, circuits_page() function which is in server.py is being called. The 'addcircuit' if conditional will be triggered then. In this conditional first
   variables which are being taken from html page is settled to according variables and then those variables are sent to add_circuit function of my Circuit class as arguements. In add_circuit function; a connection to circuits table is beng made and insert query is being called in
   order to add the following row to the table. Here ,as I mentioned earlier, text information is uppercased by .upper() function and then inserted to the table.

Update Method Implemtation
,,,,,,,,,,,,,,,,,,,,,,,,,,
   As the user fills the updated information and the id of the intended row to update and presses the 'Update Circuit' button.Then  circuits_page() function is being called from server.py . The 'updatecircuit' if conditional is invoked and the same steps are being taken as add method. The only significant
   change is the passing of the id variable to update_circuit function in Circuit class. Then update_circuit runs update query where the id is equal to the user's id input. After the query is done function redirects to circuits_page() as return statement.



Race Class Table Contents
-------------------------
* **id:** primary key of the table as serial type
* **name:** represents the name of the race as text which can not be NULL
* **fastest_lap_time:** keeps the fastest lap time information  of the race as integer which is 0 by default and in terms of seconds
* **winners_average_lap_time:**   keeps the winner's average lap time information of the race as integer which is 0 by default and in terms of seconds
* **average_lap_time:** keeps the general average lap time information of the race as integer which is 0 by default and in terms of seconds
* **first_position:** keeps the name of the first position information of the racer as integer which can not be NULL
* **track_circuit_id:** it is the foreign key that references circuits table's id column.
* **number_of_laps:** keeps the number of laps that takes place in that race which can not be NULL and kept as text
* **total_accidents:** keeps the total accident count of the race as integer variable which has 0 as default value

Note About The Table:
,,,,,,,,,,,,,,,,,,,,,
   At the start of my races_page() function in server.py related Race class object is being created. The related if clauses' function calls are being held by this instantiated
   object later on as return statements.(Same as Circuit class)

Race Class Methods' Implementations
-----------------------------------

Search Method Implementation:
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   Global variable search_bool which is 0 by default is being kept as the identifier for my if conditions. search_name which is empty text is also kept for storing
   the intended text for searching. As the user enters the text of interest in the search area and presses the search button at my races.html interface, the function
   races_page() is being called from server.py document. It enters the 'searchrace' if condtional and gets the data from html document and runs the search_race function
   of my Race class. My search_race function takes self and name as an arguement and changes search_bool to 1 and changes the entered text to upper for case insensitive search.

   My function redirects to my races_page as a return operation. From here my list_page() function is being used for printing the intended search variable. I implemented an if conditional that looks
   if search_bool is 1. If so it selects the rows where the intended search text is present in any location of th name variable of races table. It is being done by using LIKE and '%' commands as prefix and postfix
   of the search_name variable. If there are multiple outputs, outputs are being printed in ascending order.

Delete Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   My delete function works as the user enters the id of the unwanted entry and presses the delete button in my html form. As soon as the user does that my races_page() function in server.py is being called by my html form and it
   enters the 'deleteracewithid' if conditional. from here it sends the id variable to my delete_race_with_id function which is in my Race class. In delete_race_with_id(self,id) function a connection to races table is being created
   and deletion operation is being done by delete query of sql language where the id is equal to the input which is entered by the user. Then redirection to the races_page is being done by return statement of the function.

Add Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,
   As soon as the user fills all the related row information on the html page and presses the 'Add Race' button, races_page() function which is in server.py is being called. The 'addrace' if conditional will be triggered then. In this conditional first the
   variables which are being taken from html page is settled to according variables and then those variables are sent to add_race function of my Race class as arguements. In add_race function; a connection to races table is beng made and insert query is being called in
   order to add the following row to the table. Here ,as I mentioned earlier, text information is uppercased by .upper() function and then inserted to the table.

Update Method Implemtation
,,,,,,,,,,,,,,,,,,,,,,,,,,
   As the user fills the updates information and the id of the intended row to update  and presses the 'Update Race' button, races_page() function is being called from server.py . The 'updaterace' if conditional is invoked and the same steps are being taken as add method. The only significant
   change is the passing of the id variable to update_race function in Race class. Then update_race runs update query where the id is equal to the user's id input. After the query is done function redirects to races_page() as return statement.


Accident Class Table Contents
-----------------------------
* **id:** primary key of the table as serial type
* **rider_name:** represents the first name of the racer that took place at the accident as text which can not be NULL
* **rider_surname:** represents the last name of the racer that took place at the accident as text which can not be NULL
* **race_id:** it is the foreign key that references races table's id column.
* **is_fatal:** keeps the information of the fatality condition of the accident


Note About The Table:
,,,,,,,,,,,,,,,,,,,,,
   At the start of my Accidents_page() function in server.py related Accident class object is being created. The related if clauses' function calls are being held by this instantiated
   object later on as return statements.(Same as Circuit and Race classes)

Accident Class Methods' Implementations
---------------------------------------
Search Method Implementation:
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   Global variable search_bool which is 0 by default is being kept as the identifier for my if conditions. search_name which is empty text is also kept for storing
   the intended text for searching. As the user enters the text of interest in the search area and presses the search button at my accidents.html interface the function
   Accidents_page() is being called from server.py document. It enters the 'searchAccident' if condtional and gets the data from html document and runs the search_Accident function
   of my Accident class. My search_Accident function takes self and name as an arguement and changes search_bool to 1 and changes the entered text to upper for case insensitive search.


   My function redirects to my Accidents_page as a return operation. From here my list_page() function is being used for printing the intended search variable. I implemented an if conditional that looks
   if search_bool is 1. If so it selects the rows where the intended search text is present in any location of th name variable of Accident table. It is being done by using LIKE and '%' commands as prefix and postfix
   of the search_name variable. If there are multiple outputs, outputs are being printed in ascending order.

Delete Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,,,,
   My delete function works as the user enters the id of the unwanted entry and presses the delete button in my html form. As soon as the user does that my Accidents_page() function in server.py is being called by my html form and it
   enters the 'deleteAccidentwithid' if conditional. From here it sends the id variable to my delete_Accident_with_id function which is in my Accident class. In delete_Accident_with_id(self,id) function a connection to Accident table is being created
   and deletion operation is being done by delete query of sql language where the id is equal to the input which is entered by the user. Then redirection to the Accidents_page is being done by return statement of the function.

Add Method Implementation
,,,,,,,,,,,,,,,,,,,,,,,,,
   As soon as the user fills all the related row information on the html page and presses the 'Add Accident' button, Accidents_page() function which is in server.py is being called. The 'addAccident' if conditional will be triggered then. In this conditional first the
   variables which is being taken from html page is settled to according variables and then those variables are sent to add_Accident function of my Accident class as arguements. In add_Accident function; a connection to Accident table is beng made and insert query is being called in
   order to add the following row to the table. Here ,as I mentioned earlier, text information is uppercased by .upper() function and then inserted to the table.

Update Method Implemtation
,,,,,,,,,,,,,,,,,,,,,,,,,,
   As the user fills the updated information and the id of the intended row to update and presses the 'Update Accident' button, Accidents_page() function is being called from server.py . The 'updateAccident' if conditional is invoked and the same steps are being taken as add method. The only significant
   change is the passing of the id variable to update_Accident function in Accident class. Then update_Accident runs update query where the id is equal to the user's id input. After the query is done function redirects to Accidents_page() as return statement.


Initialize Table Method
,,,,,,,,,,,,,,,,,,,,,,,
   I also implemented a function in my dropdown list  which basically drops all tables in order of Accidents first, races second and ciruits last. Then creates tables in reverse order with adding hardcoded basic rows to them. When user presses the corresponding text
   in my dropdown list, resetmemmi() function in server.py is being called. In this function reset_memmi class's list_page() function is called and then a redirection to the home page of the website is being done by return statement. In reset_memmi class ,which is in erase_refill.py file, list_page() function does what
   I explained before. This function returns no arguement or operation.


General Look To HTML Structure
------------------------------
   Html structure of all tables are similar to each other. It lists the related table at the top and then update methods block followed by add method block followed by search block and delete block at the end.

