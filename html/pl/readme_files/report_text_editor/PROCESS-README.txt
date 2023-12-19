Report Text Editor
Author: Nick Bild
Date: 2017-06-19

Description
--------

The Report Text Editor will let you add/edit text blocks that are inserted into the report in defined regions (as selected by user).

Script relationships:

form.cgi
|
-- edit.cgi

Dependencies
--------

Perl v5 is required.

Software installed on yonggan (192.168.0.16) in /home/yonggan/www/pl/report_text_editor.

Usage Instructions
--------

The Report Text Editor is available on the ORB intranet:

http://192.168.0.16 -> Sequencing -> Report Text Editor

You'll be asked the following questions:

* Choose existing stored text to edit

Choose an existing entry if you would like to EDIT it.  The type of each entry is shown in brackets ("[]") before the user-defined title.  The type determines which area of the report it is inserted into.

* Add new stored text:

If you want to ADD a new stored text block, select a type (which determines which area of the report it is inserted into) and enter a descriptive title.

Clicking next will bring up an HTML editor.  Edit the HTML as desired, then click "Save" to store the entry in the database for use with the report generator.

Scripts
--------

* form.cgi - Collect user input.

* edit.cgi - Allow user to edit HTML and save edits to database.

