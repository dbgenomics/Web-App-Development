Correlation Matrix
Author: Nick Bild
Date: 2016-03-21
Version 1.0: Initial development.
UPDATE 2016-04-14: Nick Bild
Version 1.1: Add web support.

Description
--------
The correlation matrix analysis tool processes raw data according to user input for analsis via an R script developed by Kevin Ogden.

Script relationships:

WEB:

form.html
|
-- api.cgi
   |
   -- correlation.pl
   |  |
   |  -- corrmat.R
   |
   -- status.cgi

COMMAND LINE:

correlation.pl
|
-- corrmat.R

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  The following R libraries are required:

magrittr
ggplot2
RColorBrewer
reshape2
dplyr

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

9. correlation matrix

The following questions will be asked:

Specify the data file (including the full path):
 e.g.: easyRNASeq_Filter_Martinez-Nunez_genes_rpkm.txt
Is the data already log transformed (Y/N)?
 e.g.: N
Which columns in the sampleinfo file should be combined to name the samples (comma-separated list, e.g.: 6,7,8)?
 e.g.: 6,7,8
Limits to use for coloring the correlation matrix. Specify values as 'min,max'. To use ggplot's default, leave this blank.
 e.g.: none
Specify the output figure width (default: 800)?
 e.g.: 800
Specify the output figure height (default: 600)?
 e.g.: 600
In which column does your data begin?
 e.g.: 9
What method would you like to use to cluster samples?
 e.g.: none

Output will be placed in a folder named "correlation" under the current working directory.

* The pipeline is also available as part of the ORB Intranet:

http://192.168.0.16/ -> Statistics -> Correlation Matrix

* Alternatively, to run the pipeline manually:

./correlation.pl sampleinfo.txt

Sample Info File:

The sample info file may contain a 10th column that directs the ordering of the samples.  Here is an example:

#Sequencing Data ID	Sample Name	ORB Enriched DNA Library ID	Customer ID	Project	Factor 1	Factor 2	Factor 3	Subject	Order
SL145888	3727-CN-0001	CM4910801	A012L8XTD	Bista	A1	B1	C1	S1	1
SL145889	3727-CN-0001	CM4910801	A012L8XTD	Bista	A2	B1	C1	S1	2
SL145890	3727-CN-0001	CM4910801	A012L8XTD	Bista	A3	B1	C1	S1	3
SL145891	3727-CN-0001	CM4910801	A012L8XTD	Bista	A4	B1	C1	S1	4
SL145892	3727-CN-0001	CM4910801	A012L8XTD	Bista	A5	B1	C1	S1	5
SL145893	3727-CN-0001	CM4910801	A012L8XTD	Bista	A6	B1	C1	S1	6
SL145894	3727-CN-0001	CM4910801	A012L8XTD	Bista	A7	B1	C1	S1	7
SL145895	3727-CN-0001	CM4910801	A012L8XTD	Bista	A8	B1	C1	S1	8

Samples in the output file will be ordered in ascending order according to the value in the 10th, or higher, column if it is named "Order".  If this value is not present, samples will be ordered in the same order that they appear in the sampleinfo file.

Scripts
--------

* correlation.pl - This collects user input, transforms the input data appropriately, and launches corrmat.R.

* corrmat.R - Kevin Ogden's correlation matrix analysis script.

* form.html - Collect user input.

* api.cgi - Launch marburg job from web.

* status.cgi - Check status of marburg job and allow for download of results on web.
 
