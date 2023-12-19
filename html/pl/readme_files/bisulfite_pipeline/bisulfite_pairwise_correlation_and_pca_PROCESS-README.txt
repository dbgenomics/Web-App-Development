Bisulfiteseq Pairwise Correlation and PCA
Author: Nick Bild
Date: 2016-08-10
Version 1.0: Initial development.

Description
--------

Bisulfiteseq Pairwise Correlation and PCA generates a pairwise Pearson's correlation coefficient matrix, and produces hierarchical clustering and PCA images.

Script relationships:

bismark_methyl_pct_correlation_run.pl
|
-- bismark_methyl_pct_correlation.pl

Dependencies
--------

Perl v5 is required.  R version 3.0.1 is required, as well as the "methylKit" library.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* Bisulfiteseq Pairwise Correlation and PCA is available via the bisulfiteseq pipeline (note that step numbers may change over time):

10. pairwise correlation and PCA

* Output

Relative to the project directory, the following files will be generated:

correlation/correlation_results.txt			-- Pairwise correlation results, list format.
correlation/correlation_results_matrix.txt		-- Pairwise correlation results, matrix format.
correlation/cluster.png					-- Hierarchical clustering.
correlation/pca.png					-- PCA

Scripts
--------

* bismark_methyl_pct_correlation_run.pl - Set up environment and launch jobs.

* bismark_methyl_pct_correlation.pl - Generates a pairwise Pearson's correlation coefficient matrix, and produces hierarchical clustering and PCA images.

