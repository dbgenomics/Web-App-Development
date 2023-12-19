Bisulfiteseq Fisher's Exact Test
Author: Nick Bild
Date: 2016-08-10
Version 1.0: Initial development.

Description
--------

Bisulfiteseq Fisher's Exact Test runs Fisher's exact test for all groups.

Script relationships:

bismark_methyl_fisher.pl

Dependencies
--------

Perl v5 is required. R version 3.0.1 is required, as well as the "methylKit" library.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* Bisulfiteseq Fisher's Exact Test is available via the bisulfiteseq pipeline (note that step numbers may change over time):

11. fisher's exact test

The following questions will be asked:

- Enter a comma-delimited list of control samples (no spaces, e.g.: SL156411,SL156412)

* Output

Relative to the project directory, the following files will be generated:

fisher/fisher_<GROUPNAME>.txt

Sampleinfo:

Groups must be defined in the sampleinfo file, in a column named "Group".

Scripts
--------

* bismark_methyl_fisher.pl - Runs Fisher's exact test for all groups.

