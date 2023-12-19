General Statistical Analysis Sort
Author: Nick Bild
Date: 2016-04-04
Version 1.0: Initial development.

Description
--------

The General Statistical Analysis Sort tool sorts data according to user specifications.

Script relationships:

tophat_general_stat_sort.pl

Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/.

Usage Instructions
--------

* The pipline is available as part of statanalysis:

6. sort general statistical analysis

The following questions will be asked:

Enter the data file (with absoulte path) of the file you want to sort:
 e.g.: Stat_easyRNASeq_Filter_Hans_genes_rpkm_sample-infor-Hans_3771_Tukey_combined.txt
Enter comma-delimited list of sampleinfo column numbers to sort by. Use "x" to indicate an interaction (e.g.: 6,7,8,6x7,6x8,7x8):
 e.g.: 6,7,6x7

Input – standard pipeline input, statanalysis output file to analyze, column of variables to be used to calculate the minimum ANOVA P with/ without interaction. Possible entries would be one or more of the following:  6,7,8,6x7,6x8,7x8. The “x” indicates an interaction for the two variables.

Computation - Using the ANOVA P columns for the designated variable, calculate the minimum value. Ignore non-numeric values in the ANOVA P columns but if all values are non-numeric for a row, assign a value of 1 for the minimum value. Sort the rows based on the minimum ANOVA P value that is calculated.

Output - In the same directory as the original file - Re-sorted statanalysis result file, with “resorted_” added to the name as a prefix.

Scripts
--------

* tophat_general_stat_sort.pl - Collect user input, and sort data file accordingly.

