Data Analysis Apps
Author: Nick Bild
Date: 2016-05-19
Version 1.0: Initial development.

Description
--------

Data Analysis Apps are a set of data analysis tools available to clients via a public website.

Script relationships:

data-analysis-apps.php

principal-comp-analysis.php
|
-- pca_api.cgi
   |
   -- pca_status.cgi

hierarchical-clustering.php
|
-- clustering_api.cgi
   |
   -- clustering_status.cgi

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  PHP v5 is required.

Required R modules (on fileserver):
rvest
xml2
httr
magrittr
dplyr
reshape2
docopt
XML

Web front-end software is installed on T550-ORB-company-files (192.168.0.18) in /var/www/html/.

Data analysis back-end software is installed on fileserver (10.1.10.104) in /home/nick/.

Configuration
--------

NOTE:  Computation takes place on fileserver (10.1.10.104).  For specific details on each tool (Principal Components Analysis, Hierarchical Clustering, ...) see the relevant documentation for that tool.  This documentation deals with the Data Analysis apps framework.

The website is available at:

http://192.168.0.18/data-analysis-apps.html

It is available via the menu at:

Support -> Data Analysis Apps

Apache2 Config:

CGI script execution needs to be enabled.  In /etc/apache2/apache2.conf, add:

AddHandler cgi-script .cgi .pl

In this Directory block:

<Directory /var/www/html/>
        Options Indexes FollowSymLinks ExecCGI
...

Add "ExecCGI".

From the command line, enable the CGI module:

sudo ln -s /etc/apache2/mods-available/cgid.load /etc/apache2/mods-enabled/
sudo ln -s /etc/apache2/mods-available/cgid.conf /etc/apache2/mods-enabled/

Allow The Apache User To ssh To The Computation Server:

In /etc/passwd:
Set "/bin/bash" as shell for www-data.

Create an rsa key pair:
sudo mkdir /var/www/.ssh
sudo chown -R www-data. /var/www/.ssh
sudo -u www-data ssh-keygen -t rsa

Add public key to authorized keys in 10.1.10.104.

ssh from 192.168.0.18 to 10.1.10.104, accept fingerprint when prompted:
Are you sure you want to continue connecting (yes/no)? yes

Scripts
--------

* data-analysis-apps.php - Landing page.  Allows user to pick tool.

* principal-comp-analysis.php - PCA data collection form.

* pca_api.cgi - Remotely execute a PCA.

* pca_status.cgi - Monitor remote PCA job, alert user when complete, and present results for download.

* hierarchical-clustering.php - Clustering data collection form.

* clustering_api.cgi - Remotely execute a clustering job.

* clustering_status.cgi - Monitor remote Clustering job alert user when complete, and present results for download.

