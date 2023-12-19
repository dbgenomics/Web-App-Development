Plot Top 10 Genes
Author: Nick Bild
Date: 2016-03-22
Version 1.0: Initial development.
UPDATE 2016-04-14: Nick Bild
Version 1.1: Add web support.
UPDATE 2016-07-12: Nick Bild
Allow user to specify ordering of groups via sampleinfo file.
UPDATE 2016-08-19 NAB
Specify which sampleinfo columns contain factors in R script arguments.

Description
--------
The Plot Top 10 Genes analysis tool processes raw data according to user input for analsis via an R script developed by Kevin Ogden.  The R script produces graphical plots to visualize the data.

Script relationships:

WEB:

form.html
|
-- api.cgi
   |
   -- plot_top_genes.pl
   |  |
   |  -- plot_top10_seqs.R
   |
   -- status.cgi

COMMAND LINE:

plot_top_genes.pl
|
-- plot_top10_seqs.R

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  The following R libraries are required:

docopt
reshape2
dplyr
stringr
ggplot2
grid

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

10. plot top genes

The following questions will be asked:

Specify the data file (including the full path):
 e.g.: easyRNASeq_Filter_Martinez-Nunez_genes_rpkm.txt
Is the data already log2 transformed (Y/N, default: N)?
 e.g.: N
Which column contains the gene names?
 e.g.: 1
Which columns should be used to sort the data (comma-separated list, e.g.: 6,7,8)?
 e.g.: 10
Should the data be sorted in ascending (default) or descending order (A/D)?
 e.g.: A
How many genes should be plotted (default: 10)?
 e.g.: 10
What type of expression data is this (for y-axis label, default: RPKM)?
 e.g.: RPKM
Specify the output figure width (default: 1800)?
 e.g.: 1800
Specify the output figure height (default: 1500)?
 e.g.: 1500
What type of plot would you like 1)schematic plot 2)standard boxplot 3)scatter plot (default: 1)?
Enter NUMBER:
 e.g.: 1
In which column does your data begin?
 e.g.: 9

Output will be placed in a folder named "top10_plots" under the current working directory.

* The pipeline is also available as part of the ORB Intranet:

http://192.168.0.16/ -> Statistics -> Plot Top Genes

* Alternatively, to run the pipeline manually:

./plot_top_genes.pl sampleinfo.txt

Sampleinfo:

The sampleinfo file must be a tab-delimited text file.
An optional "Order" column may be supplied in column 5 to control the order of the
factors in the output. Each sample for a given factor should have the same order number.

Scripts
--------

* plot_top_genes.pl - This collects user input, transforms the input data appropriately, and launches plot_top10_seqs.R.

* plot_top10_seqs.R - Kevin Ogden's top gene plotting script.

* form.html - Collect user input.

* api.cgi - Launch marburg job from web.

* status.cgi - Check status of marburg job and allow for download of results on web.
 
