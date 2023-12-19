Bisulfite Conversion Report
Author: Nick Bild
Date: 2016-07-25
Version 1.0: Initial development.

Description
--------

Bisulfite Conversion Report generates a report summarizing bisulfite base conversions in the samples as compared to the unconverted reference sequence.  Statistics are based on a random 1% sampling of each sample.

Script relationships:

bisulfite_conversion_report_run.pl
|
-- bisulfite_conversion_report.pl

Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* Bisulfite Coverage Report is available via the bisulfiteseq pipeline (note that step numbers may change over time):

6. bisulfite conversion report

The following questions will be asked:

- Selections for the following keys from oap_database.txt will need to be made:

INDEXED_FASTA			-- samtools indexed fasta file of an unconverted reference genome.

* Output

Relative to the project directory, the following files will be generated:

- bisulfite_conversion_report.txt

Bisulfite conversion statistics for each sample.

- <SAMPLE>_cpg_sites.txt

CpG site statisitcs for use in downstream steps.  Statistics are based on a random 1% sampling of each sample.

Scripts
--------

* bisulfite_conversion_report_run.pl - Set up environment and launch jobs.

* bisulfite_conversion_report.pl - Generate conversion statistics for a sample.

