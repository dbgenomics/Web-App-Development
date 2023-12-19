Venn Diagram
Nick Bild
2017-06-22
Version 1.0 Initial documentation.

Description
--------

The Venn Diagram app will filter an expression data set per user-specified criteria, and determine which of the filtered genes are detectable (from threshold file) on a per-group basis (group average will be compared to the threshold group average).  The number of detectable genes per group will be plotted in a Venn diagram.

Script relationships:

venn.pl

Dependencies
--------

Perl v5 is required. R v3.2.2 is required, with the "VennDiagram" library.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

The Venn Diagram app is available as part of the statanalysis pipeline (note that step numbers may change over time):

14. Venn diagram

You'll be asked the following questions:

* Enter the data file (including the full path, e.g.: /path/to/file.txt):
e.g.: /home/act/datatest/2017-06-13_venn_diagram_app/2016-12-27_Filter_Genes_RPKM_Stat-Results.txt

* Enter the exact name of your filter column:
e.g.: ANOVA P: Group
This must match a column header in the data file exactly.

* Enter the filter threshold (the actual value must be < this value for the gene to be retained):
e.g.: 0.05

* If you want to filter by fold change, enter the threshold here (the max FC must be > this value for the gene to be retained):
e.g.: 1

* Enter the threshold file (including the full path, e.g.: /path/to/file.txt):
e.g.: /home/act/datatest/2017-06-13_venn_diagram_app/2016-12-27_Lincoln_mRNA-Seq_threshold.txt

* Enter the row number from the threshold file to use:
e.g.: 4

* Enter a comma-separated list of groups (from the required 'Groups' column of sampleinfo file) to include in Venn diagram:
e.g.: Day5,Day8,Nod DMSO
These must match group names from the "Groups" column of the sampleinfo file exactly.

* Enter a comma-spearated list of colors to use, 1 for each group (Leave blank for default. See /home/act/software/nickbild/Rcolor.pdf for valid color names.):
e.g.: chartreuse2,tomato3,deepskyblue3

Data File
--------

The data file must be a tab-delimited text file.

The first row must contain a header with column names.  Gene names must be in the first column.  If using the filter by fold change option, all fold change columns in the data file MUST begin with "Fold Change".

Sampleinfo
--------

The sampleinfo file MUST contain a header row with a column named "Group".  Samples will be grouped according to this column.

Sample names must be in the first column, and must match the sample names in the data file header.

Output
--------

<PROJ_DIR>/venn/venn_<SELECTED-GROUPS>.png					-- Venn diagram of detectable genes per group.
<PROJ_DIR>/venn/filtered_data_for_venn_diagrams.txt				-- Data source used to create Venn diagram.

Scripts
--------

* venn.pl - Collect and process user input and generate Venn diagram.

