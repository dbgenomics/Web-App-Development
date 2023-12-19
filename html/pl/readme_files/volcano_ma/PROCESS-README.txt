Volcano and MA Plot Generator
Author: Nick Bild
Date: 2017-08-10

Description
--------

The Volcano and MA Plot Generator will create volcano and MA plots for general stat analysis result files.

Script relationships:

volcano_ma_plots.pl

Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/.

Usage Instructions
--------

The mRNA-seq Report Generator is available as part of the statanalysis pipeline (note that step numbers may change over time):

15. volcano and MA plots

You'll be asked the following questions:

* Enter the name of the stat analysis data file (including full path, e.g.: /path/to/file.txt):

* For the volcano plot, enter the exact name of the Tukey P value column (*Leave blank to automatically analyze all Tukey P/Fold Change pairs*):

Enter this to only run the plot for a specific column, or if non-standard column names (that the script can't autodetect) were used in the data file column headers.

If a p-value column was entered, you'll be asked:
* For the volcano plot, enter the exact name of the fold change column:

* Enter a width, in pixels, for the output images (Leave blank to use 2400):

* Enter a height, in pixels, for the output images (Leave blank to use 2400):

Algorithm Details
--------

* Volcano plot data points are calculated as:

-log10(P value) versus log2(Fold Change)

and p-values <= 0.05 will be shown in red.

* MA plot data points are calculated as:

0.5*(log2(grpA_ave) + log2(grpB_ave)) versus log2(grpA_ave) - log2(grpB_ave)

where grpA and grpB are groups taken from columns 6-8 of the sampleinfo file.  All pairwise group combinations will be performed.

Sampleinfo File
--------

A standard sampleinfo file is expected, with sample names in the first column (that match expression value column headers in the data file) and group names in columns 6-8.  If all columns are not needed for grouping, they can be left blank, or marked "NA", for all samples.

Output
--------

<PROJ_DIR>/volcano_plots/<TUKEY_COLUMN_NAME>_volcano_plot.jpg				-- Volcano plot, by Tukey P / fold change pair.
<PROJ_DIR>/ma_plots/<GROUP1>_vs_<GROUP2>_mean_diff_plot.jpg				-- MA plot, by pairwise group combinations.

Scripts
--------

* volcano_ma_plots.pl - Generate volcano and MA plots from general stat analysis data file.

