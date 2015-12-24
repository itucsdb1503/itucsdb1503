Developer Guide
===============

Database Design
---------------

Our database consists of 12 tables distributed evenly among 4 members. Individual members have refences between their tables however there are no references between different member's tables.

**Note:** At the beginning of the project we distributed topics among the team members. However one of our members ended up not participating in the project. We didn't know if he would start the project at any point so we didn't refence other members tables in our tables. As the project deadline came closer we gave up on connecting tables to each other where possible because everybody had made different adjustments.

 .. figure:: images/database_diagram.png
      :align: center
      :alt: can not load image

      Database Diagram

Code
----

   Our project uses the implementation of flusk between python based server configuration and HTML pages. We use flusk request.form method to
   call different python functions from corresponding classes and vice versa sends results from python functions to HTML pages by using the
   render_template method from flusk. For SQL we used PostgreSQL database system with query entries from python class functions for the corresponding SQL
   tables.

.. toctree::

   member1
   member2
   member3
   member4
   member5
