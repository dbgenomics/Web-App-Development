Backup Public Website
Author: Nick Bild
Date: 2016-04-19
Version 1.0: Initial development.

Description
--------

The Backup Public Website tool backs up the files and databases running http://oceanridgebio.com/ to Amazon S3.  The 4 most recent backups are retained.

Backups contain an SQL dump of all databases, and all files at /home/oceanrid, excluding public_ftp and Retired-Web-Files.

Script relationships:

backup.pl

Dependencies
--------

Perl v5 is required.  Amazon AWS command line tools are required.

Software installed on oceanridgebiosciences.com (67.225.129.9) in /home/oceanrid.

Usage Instructions
--------

The backup script on oceanridgebiosciences.com automatically runs (via a cron job) every Sunday at 1:00 AM.  It saves a new backup, and maintains the 4 most recent backups, in /home/oceanrid/full_backup/.  This directory is then synchronized with the Amazon S3 bucket s3://orb-web-backup.

To edit the cron schedule, log in to the webserver as user oceanrid, and type:

crontab -e

Scripts
--------

* backup.pl - Saves a new backup, and maintains the 4 most recent backups, in /home/oceanrid/full_backup/.  This directory is then synchronized with the Amazon S3 bucket s3://orb-web-backup.

