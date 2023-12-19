Project Backup Pipeline
Author: Nick Bild
Date: 2016-02-09
Version 1.0: Initial development.
Specifications at ORB-Computational-Methods/General-Methods/2016-02-08_Cluster-Backup-Specifications.docx

Description
--------

The Project Backup Pipeline backs up project directories on the westnile and marburg clusters.  Data is backed up to norwalk.  Project directories backed up on marburg are located in:

/home/act/data
/storage01

and on westnile:

/home/act/data
/westnile/cluster/projects

The timestamp on a project directory must be at least 2 days old to be included in the backups automatically.  If it is not, the user will be prompted to decide if the project directory should be included or not.

Script relationships:

backup_marburg.pl

backup_westnile.pl

Dependencies
--------

Perl v5 is required.  The DateTime module is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild and westnile (192.168.0.6) in /home/act/software/nickbild.

Usage Instructions
--------

* To run the pipeline manually:

cd /home/act/software/nickbild

On marburg:
./backup_marburg.pl

On westnile:
./backup_westnile.pl

If there is not enough working space in a project directory to compress any of the projects scheduled for backup, the process will exit and inform the user that they must free up some disk space in that location, then run the backup again.

* Output

Output is written in the current working directory, to <timestamp>-archive.txt.  It will contain the following sections:

 Backups Needed - This lists the project directories that need to be backed up, whether they are new or updates, and which cluster they are on.

 Excluded Directories - These project directories will be excluded, and the reason for exclusion (insufficient disk space, too recent of a timestamp, ...) is listed.

 Backing Up - This is a log of the activities related to the backup of project directories that were included in this batch.  MD5 checksums are included to ensure the backup completed correctly.  Be sure to check this section for any errors that require action to correct, such as an MD5 mismatch.

Projects are backed up to norwalk:/cluster/backup unless sufficient free space is not available.  In that case, projects are backed up to norwalk-2:/cluster/backup.

Scripts
--------

* backup_marburg.pl - Backup marburg project directories.

* backup_westnile.pl - Backup westnile project directories.

