Parts Implemented by Göktuğ Öcalan
==================================

Access
------
Accessing my parts in the website is pretty simple. The user can hover over the "Teams&Countries" section in the navigation bar and select their intended page from the dropdown menu.

 .. figure:: images/navbar_teams_dropdown.jpg
      :align: center
      :alt: can not load image

      Dropdown Menu on the Navigation Nar

General
-------
User interface that is provided for my parts of the code is made to look simple and accessible. The tables and all their operations are contained in one page for each table. This allows for ease of use.

 .. figure:: images/page_teams.jpg
      :width: 995px
      :height: 500px
      :align: center
      :alt: can not load image

      Teams Page

Teams Page
----------
Teams page holds the teams table and forms for all the operations the table supports.

 .. figure:: images/table_teams.jpg
      :align: center
      :alt: can not load image

      Teams Table

Team Forms
,,,,,,,,,,
Available operations for this table are:

- Add
- Update
- Delete
- Search
- Reset

**Add:** All fields except "Number of Riders" accepts text input. All input will be automatically converted to upper case. The "Country" field has to be filled with an existing country abbrevation from the "countries" table.

**Update:** ID is used as the identifying attribute to select which tuple to update. The user have to enter the old information for the parts he doesn't want to update.

**Delete:** The tuple with the entered ID is deleted from the table.

**Search:** Any number of fields in the form can be filled. Given parameters will be searched in the attributes of the tuples, partial matches will also be showed. Refreshing the page after a search will list the full table again.

**Reset:** This button drops and recreates all three tables that are implemented by me in the project.

 .. figure:: images/form_teams.jpg
      :width: 1309px
      :height: 275px
      :align: center
      :alt: can not load image

      Team Forms

Countries Page
--------------
Countries page holds the countries table and forms for all the operations the table supports.

 .. figure:: images/table_countries.jpg
      :align: center
      :alt: can not load image

      Countries Table

Country Forms
,,,,,,,,,,,,,
Available operations for this table are:

- Add
- Update
- Delete
- Search
- Reset

**Add:** All fields accepts text input. All input will be automatically converted to upper case. It is recommended to fill the "Abbrevation" field with the 3 letter abbrevations provided by International Standards Organization.

**Update:** Name is used as the identifying attribute to select which tuple to update. A new name can be entered. The user have to enter the old information for the parts he doesn't want to update.

**Delete:** The tuple with the entered name is deleted from the table.

**Search:** Any number of fields in the form can be filled. Given parameters will be searched in the attributes of the tuples, partial matches will also be showed. Refreshing the page after a search will list the full table again.

**Reset:** This button drops and recreates all three tables that are implemented by me in the project.

 .. figure:: images/form_countries.jpg
      :align: center
      :alt: can not load image

      Country Forms

Standings Page
--------------
Standings page holds the standings table and forms for all the operations the table supports.

 .. figure:: images/table_standings.jpg
      :align: center
      :alt: can not load image

      Standings Table

Country Forms
,,,,,,,,,,,,,
Available operations for this table are:

- Add
- Update
- Delete
- Search
- Reset

**Add:** All fields except name accepts integers. All input will be automatically converted to upper case. Position has to be unique in the table.

**Update:** Position is used as the identifying attribute to select which tuple to update. A new position can be entered. The user have to enter the old information for the parts he doesn't want to update.

**Delete:** The tuple with the entered position is deleted from the table.

**Search:** Any number of fields in the form can be filled. Given parameters will be searched in the attributes of the tuples, partial matches will also be showed. Refreshing the page after a search will list the full table again.

**Reset:** This button drops and recreates all three tables that are implemented by me in the project.

 .. figure:: images/form_standings.jpg
      :align: center
      :alt: can not load image

      Standing Forms

