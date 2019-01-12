# sqldoc
Utility that generates HTML documentation for database tables based on commented DDL statements

## usage notes
* set up config/main_config.yaml
* run main.py to produce the updated version of the documentation
* open table_catalog.html

There are checkboxes to the left from the column names.
Clicking on these checkboxes produces a popup with a SELECT query containing columns that are checked.
Clicking on the popup copies the query to your buffer and hides the popup.

## files description

### root
* main.py - The main script of the utility, you have to run it in Python3 to produce the updated version of the documentation. The only dependency is YAML library
### config
* main_config.yaml - YAML configuration file that contains all necessary settings to run the utility. 
Every setting is commented in the file, please refer to the file itself for additional details.
* catalog_template.html - Template of the HTML file that contains the documentation table. 
It's a simple table with a fixed header.
### example
This folder has the sample SQL scripts that show the principle of the markdown.
* 01_simple_table.sql - The most basic DDL statement
* 02_more_complex_table.sql - If you have a larger table where columns can be logically divided into groups you can add a comment before each group of columns that will produce a section row in the table (see the output).
### web
This folder contains the document page:
* sqlpopup.js -jQuery function that is responsible for sql query popup
* table_catalog.css - The stylesheet of the table
* table_catalog.html - **generated output of the utility**
