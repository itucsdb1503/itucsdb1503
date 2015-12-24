Parts Implemented by Göktuğ Öcalan
==================================

Parts implemented by me are the teams, countries and standings classes and tables. Their operations, html and css files are also implemented by me.

All Class Functions
-------------------

Functions in this segment are identical in all classes.

createTable:
,,,,,,,,,,,,

This function creates all 3 tables if they don't already exist.

dropTable:
,,,,,,,,,,

This function drops all 3 tables

initTable:
,,,,,,,,,,

This function first drops the tables and then creates them by calling the necessary functions. After that it inserts predetermined values to all three tables.

Class Specific Functions
------------------------
Functions in this section are similar but have small differences based on the attributes of the table they belong to. Also every function that returns some information for the html code also returns the current time so the navigation bar can use it.

loadPage:
,,,,,,,,,

This function is called every time the specific url for the class is requested. It either selects the entire database or it performs a filtered select on the database based on predetermined parameters. It returns the resulting relation.

addClassName(AddTeam, AddCountry, AddStanding):
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This function is called when the correspongin addClassName form is sent from the html code. It is called from server.py and the information in the html form are passed as parameters. It inserts a new tuple the table with the given attributes. All text are converted to uppercase. At the end the page url is redirected to itself so it basically refreshes the page so the new values can be showed to the user through the select query inside loadPage.

updateClassName(updateTeam, updateCountry, updateStanding):
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This function is called when the correspongin updateClassName form is sent from the html code. The information in the form is passed through server.py as parameters for this function. All existing tuples that matches the parameters are updated with new attributes.

deleteClassName(deleteTeamId, deleteCountry, deleteStanding):
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This function is called when the correspongin deleteClassName form is sent from the html code. Every tuple that matches the selected attribute are deleted.

searchClassName(searchTeam, searchCountry, searchStanding):
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

This function is called when the correspongin searchClassName form is sent from the html code. Given paramters are stored as a class variable. The page is refreshed and loadPage function is called. Stored variables are used to select the intended part of the database while sending a select query. Variables are resetted to empty strings so when the page is loaded again next time full database is listed once again because empty strings exist in every tuple.