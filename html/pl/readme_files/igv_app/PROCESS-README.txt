IGV Snapshot App
Author: Nick Bild
Date: 2016-08-19
Version 1.0: Initial development.
UPDATE 2016-08-25 NAB
Update sorting to use minimum value from multiple columns.
Generate SVG images from IGV.
Format data fields and organize output into folder structure.

Description
--------

The IGV Snapshot App generates an HTML report containing data and IGV snapshots for the top 5 sorted genes (by user-defined criteria) from a data file.


Script relationships:

form1.html
|
-- form2.cgi
   |
   -- api.cgi
      |
      -- igv_app.pl
      |  |
      |  -- igv_app_report_top.html
      |  |
      |  -- igv_app_report_bottom.html
      |
      -- status.cgi

Dependencies
--------

Perl v5 is required.  IGV must be installed and running on 192.168.0.18.

To start IGV, VNC to 192.168.0.18:5901, open a terminal, and run the command:
~/IGV_2.3.74/igv.sh

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild and yonggan (192.168.0.16) at /home/yonggan/www/pl/igv_app.

Usage Instructions
--------

IGV Snapshot App is available via the ORB Intranet:

http://192.168.0.16/ -> Sequencing -> IGV Snapshot App

* The following questions will be asked:

- Select sampleinfo file:

The sampleinfo file must be of the same format that is expected for "6. general statistical analysis" from the "statanalysis" pipeline, with sample names in the first column, and grouping information in columns 6-8 (only columns with >1 unique value will be considered in the grouping). 

- Select data file: 

The file must be tab-delimited, with a header column in the first row containing sample names, and optionally may contain additional annotation fields. 
Gene IDs must be in the first column of the data rows.

- Which group would you like to select samples from:

Groups will be determined from data in sampleinfo file.

- Which columns(s) would you like to sort by (comma-separated, no spaces, exact names from data file):

- For each column entered, specify if it should be sorted in ascending or descending order (comma-separated, no spaces, 'A' or 'D', e.g.: A,D):

- Would you like to display any other data colmns (e.g. fold changes) in the report? (comma-separated, no spaces, exact names from data file):

- Enter the full path to the BAM directory on marburg:

- Select the IGV genome to use:

- Enter the report subtitle:

This will display at the top of the HTML report.

- Enter the report prefix:

This is used to name output files.

- What column number contains the feature names used to rename genes? (this might be, for example, the "Associated Gene Name" column or the "Gene Symbol" column -- leave blank to skip)

This will rename genes in the HTML report.

- Select GTF annotation file: 

* Output

- <PREFIX>_Read_Visualizations.html - HTML report for immediate viewing.

- <PREFIX>_Read_Visualizations.zip - Self contained zip of all files needed for offline viewing of report.

- settings.txt - Record of settings and files used.

Scripts
--------

* form1.html - Intitial data collection.

* form2.cgi - Collect remaining data, display options/information based on user entries in form1.html.

* api.cgi - Prepare and launch job on marburg.

* igv_app.pl - Run IGV analysis on marburg.

* igv_app_report_top.html - HTML include.

* igv_app_report_bottom.html - HTML include.

* status.cgi - Track status of marburg job and present results to user on completion.

