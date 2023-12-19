Data Center
Version 1.0: Initial build.
2016-05-06: Build new Data Center from scratch to replace previous application.

Source Code
----

Script Relationships:

data-center.php
|
-- data-center-top.php
|
-- data-center-bottom.php
|
-- data-center-manage-entire-file-server.php
|
-- data-center-share-file.php
|
-- data-center-delete-file.php
|
-- data-center-delete-file-all.php
|
-- data-center-dl.php
|
-- data-center-add-file.php
|
-- data-center-add-user.php
|
-- data-center-delete-user.php
|
-- data-center-help.php
|
-- data-center-manage-userbase.php
|
-- data-center-view-your-files.php
|
-- data-center-welcome.php

data-center.php is the central script.  Other scripts are loaded into the content area via the "page" URL variable.

Code is installed at: /var/www/html/ on 10.1.10.104.

Dependencies
----

Apache2, php5, and MySQL 5 are required.

Apache Config
----

In /etc/apache2/apache2.conf, make sure to remove "Indexes" if it exists in the options of the following directory block.  This will prevent browsing folders (important for uploaded data files).

<Directory /var/www/>
        Options FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>

Database
----

A MySQL database is installed locally on 10.1.10.104.  The database name is "datacenter".  Login credentials are:

user: root
pass: rnavirus

The database contains the following tables:

+----------------------+
| Tables_in_datacenter |
+----------------------+
| dc_files             |
| dc_user              |
| dc_user_group        |
+----------------------+

With the structures:

dc_files
+-----------+---------------+------+-----+-------------------+----------------+
| Field     | Type          | Null | Key | Default           | Extra          |
+-----------+---------------+------+-----+-------------------+----------------+
| ID        | int(11)       | NO   | PRI | NULL              | auto_increment |
| dc_userID | int(11)       | NO   |     | NULL              |                |
| name      | varchar(1000) | NO   |     | NULL              |                |
| location  | varchar(2000) | NO   |     | NULL              |                |
| dl_count  | int(11)       | NO   |     | NULL              |                |
| filesize  | int(11)       | NO   |     | NULL              |                |
| timestamp | timestamp     | NO   |     | CURRENT_TIMESTAMP |                |
+-----------+---------------+------+-----+-------------------+----------------+

dc_files stores metadata about the files and who owns them.

dc_user
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| ID         | int(11)      | NO   | PRI | NULL    | auto_increment |
| username   | varchar(100) | NO   | UNI | NULL    |                |
| firstname  | varchar(100) | NO   |     | NULL    |                |
| lastname   | varchar(100) | NO   |     | NULL    |                |
| email      | varchar(100) | NO   |     | NULL    |                |
| passwd     | varchar(100) | NO   |     | NULL    |                |
| active     | int(11)      | NO   |     | NULL    |                |
| lastlogin  | timestamp    | YES  |     | NULL    |                |
| logincount | int(11)      | NO   |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+

dc_user stores user login credentials and other metadata about users.

dc_user_group
+-----------+---------+------+-----+---------+----------------+
| Field     | Type    | Null | Key | Default | Extra          |
+-----------+---------+------+-----+---------+----------------+
| ID        | int(11) | NO   | PRI | NULL    | auto_increment |
| dc_userID | int(11) | NO   |     | NULL    |                |
| groupID   | int(11) | NO   |     | NULL    |                |
+-----------+---------+------+-----+---------+----------------+

dc_user_group specifies if a user is an administrator (groupID=1) or regular user (groupID=2).

To rebuild a new, empty database, use the SQL script contained in the same folder as this README:

data-center-mysql_2016-05-05.sql

User Files
----

Files are uploaded to:

/var/www/html/uploads/<dc_user.ID>/<dc_files.name>

All uploaded files are recorded in dc_files.

Scripts
----

data-center.php - Main controller script.  Controls database access, look of site, and loads additional functional pages in the content area.
data-center-top.php - Recreate top portion of public web site.
data-center-bottom.php - Recreate bottom portion of public web site.
data-center-manage-entire-file-server.php - Drives "Manage Entire File Server" function.
data-center-share-file.php - Drives "Share" file function.
data-center-delete-file.php - Drives "Delete" file function.
data-center-delete-file-all.php - Drives "Delete Files" function of "Manage Userbase".
data-center-dl.php - Drives "Download" file function.
data-center-add-file.php - Drives "Add New File" function.
data-center-add-user.php - Drives "Add New User" and "Modify" user function.
data-center-delete-user.php - Drives "Delete" user function.
data-center-help.php - Displays help text.
data-center-manage-userbase.php - Drives "Manage Userbase" function.
data-center-view-your-files.php - Drives "View Your Files" function.
data-center-welcome.php - Landing page on successful login.

