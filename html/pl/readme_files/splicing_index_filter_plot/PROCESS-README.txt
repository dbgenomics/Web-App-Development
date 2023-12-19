Splicing Index Filtering and Plotting Pipeline
Author: Nick Bild
Date: 2016-03-23
Version 1.0: Initial development.
Update: 2016-03-31
Version 1.1: Modified plotting code to allow up to 3 factors to be used for grouping, and 1 for subdivision of data.  Added provision for user to select data column and value for significance testing.

Description
--------

The Splicing Index Filtering and Plotting Pipeline sorts and filters a splicing index data set to retrieve the top 100 exons.  All exons for all genes contained in the top 100 exons are then obtained.  These exons are plotted graphically by gene.

Script relationships:

splicing_index_filter-plot.pl
|
-- splicing_index_all-exons.pl
|
-- easyrnaseq_plot_si_v2.pl

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  The following R libraries are required:

Hmisc

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

11. splicing index filtering and plots

* Alternatively, to run the pipeline manually:

cd /home/act/software/nickbild

./splicing_index_filter-plot.pl sampleinfo

The following questions will be asked:

Specify the data file (including the full path):
 e.g.: /path/to/splicingindex_stat_results.txt
Which columns should be used to filter the data?
(comma-separated list for each criteria, criteria separated by spaces; e.g.: 6,7,8 9 10,11)
 e.g.: 14 20,21 54
Should the data be sorted in ascending or descending order (A/D)?
(one for each criteria, separated by spaces; e.g.: A D A)
 e.g.: D A D
How many top genes should be plotted (one for each criteria, separated by spaces; e.g.: 10 12 10))?
 e.g.: 10 11 12
What column should be used to test for significance (one for each criteria, separated by spaces; e.g.: 20 21 32))?
 e.g.: 45
What value should be used to test for significance (one for each criteria, separated by spaces; e.g.: 0.05 0.1 0.05))?
 e.g.: 0.05
Which columns from the sample info file should be used for grouping?
(comma-separated list for each criteria, criteria separated by spaces; e.g.: 6,7,8 6,7 6,8)
 e.g.: 6,7

Columns 6,7, and 8 from the sampleinfo file are availble for grouping.  If all 3 are selected, groups will be built based on all 3 columns.  If only 2 are selected, the groups will be built based on those columns, and the data will be subdivided based on the 3rd column that was not selected.  A separate set of plots are generated for each subdivision of the data.  It is required that 2 or 3 columns be selected for each criteria, and the selcted columns be in the set [6,7,8].

Output will be placed in the "top_splicing_results" folder, under the current working directory:

- top_100_exons_criteria_<criteriaNumber>.txt - All exons for genes that were found in the top 100 exons list.

- criteria.txt - Listing of all criteria selected by user that compose each <criteriaNumber>.

- si_plots_criteria_<criteriaNumber> - A folder -- contains PNG images of all plots for the criteria.

Scripts
--------

* splicing_index_filter-plot.pl - Collects user input and filters data to desired exons.

* splicing_index_all-exons.pl - Finds all exons that belong to the genes in the top 100 exons list.

* easyrnaseq_plot_si_v2.pl - Generates graphical plots of filtered data.

* easyrnaseq_plot_si.pl - Historical.  Generates graphical plots of filtered data based on 2 factors only.  Significance column/value cannot be selected by user.

