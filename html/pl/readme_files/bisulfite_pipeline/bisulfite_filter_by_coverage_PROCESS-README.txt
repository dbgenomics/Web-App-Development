Bisulfiteseq Filter by Coverage
Author: Nick Bild
Date: 2016-10-24
Version 1.0: Initial development.

Description
--------

Bisulfiteseq Filter by Coverage filters nucleotide and tile level reports by minimum read coverage, per user input.

Script relationships:


Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

Bisulfiteseq Filter by Coverage is available via the bisulfiteseq pipeline (note that step numbers may change over time):

11. filter by coverage

* Values for the following entries in oap_database.txt will be asked for:

[MINREADCOVERAGE]			- Minimum read coverage for a sample to pass filter.
[MINPCTSAMPLES]				- Percentage of samples that must pass filter.

* Output

Relative to the project directory, the following files will be generated:

methylkit/cytosine-tile-level-report.filtered.txt				-- Filtered version of cytosine-tile-level-report.txt
methylkit/cytosine-nucleo-level-report.filtered.txt				-- Filtered version of cytosine-nucleo-level-report.txt

Scripts
--------

* bisulfite_filter.pl - Collects user input and filters files.

