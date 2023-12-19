BioradCFX-RT-PCR Data Analyzer
Author: Nick Bild
Date: 2016-03-03
Version 1.0: Initial development.

Description
--------
The BioradCFX-RT-PCR Data Analyzer is designed to transform raw PT-PCR data into analyzed data in tab-delimited format for importing into a spreadsheet.  Data for each spreadsheet tab is output in a different text file.  Each project is written to its own set of files.

Script relationships:

combined.pl
|
-- replaced.pl
|  |
|  -- cv.pl
|  |
|  -- mean.pl
|     |
|     -- d_ct.pl
|        |
|        -- dd_ct.pl
-- summary.pl

Dependencies
--------

Perl v5 is required.  No additional modules are needed.  The perl scripts must all be located in the same directory for proper function.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/qpcr (standalone) and also at 192.168.0.16 in /home/yonggan/www/pl/rt_pcr (web app).

Usage Instructions
--------

This application is generally called from its web interface at:

http://192.168.0.16/pl/rt_pcr/form.html

Instructions are provided at that web address.  After a successful run, output will be presented to the user in a list of hyperlinks.  Individual files (each representing the data for one spreadsheet tab for one project) can be downloaded by clicking on them, or all data files can be downloaded by clicking on "all.zip".

For manual execution, combined.pl is called with the following parameters:

./combined.pl sampleinfo.txt group control1,control2 datafile1.csv datafile2.csv, ... , datafileN.csv

* sampleinfo.txt - tab-delimited and of the standard format, with column 7 being the grouping column, and column 4 the customer ID.
Column 5 defines the project. Data for samples from different projects will be split into separate results files.
The Sample IDs in the 1st column MUST match the Sample IDs in the RT-PCR data files.
The file name must not contain spaces.

* group - column 7 from sampleinfo.txt.  For normalization during the delta-delta-CT calculation.  If no grouping, enter "nogroup" here.

* control1,control2 - a comma-delimited list of control targets, no spaces, e.g.: miR-328-3p,miR-484.

* datafile1.csv ... - Data files must be CSV format. Required fields are:
"Run Started" and "Well" (data must immediately follow "Well" and contain "Target","Sample", and "Cq").
Positive controls must be labeled "PC".
Negative controls must be labeled "NC".
Data file names must not contain spaces.

combined.pl will call all of the other scripts in turn, as indicated by the tree structure in the "Description" section above..

After a successful run, output will be available in the "run" directory that is created in the current working directory.

Scripts
--------

* combined.pl is the master script.  It outputs the file: <proj>.combined.txt, and then calls all of the subsequent steps.  See "Usage Instructions" section for usage.
* replaced.pl outputs the file: <proj>.replaced.txt
* cv.pl outputs the file: <proj>.cv.txt
* mean.pl outputs the file: <proj>.mean.txt
* d_ct.pl outputs the file: <proj>.d_ct.txt
* dd_ct.pl outputs the files: <proj>.dd_ct.pl <proj>.neg-dd_ct.pl <proj>.rq.pl
* summary.pl outputs the file: <proj>.qc_summary.txt

