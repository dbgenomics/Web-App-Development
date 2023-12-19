Bisulfite Nucleotide Level C Reports
Author: Nick Bild
Date: 2016-08-10
Version 1.0: Initial development.

Description
--------

Bisulfite Nucleotide Level C Reports gives nucelotide level reports of genomic cytosine positions and methylation status.

Script relationships:

bismark_nuc-level_methylation_run.pl
|
-- bismark_nuc-level_methylation.pl

Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* Bisulfite Coverage Report is available via the bisulfiteseq pipeline (note that step numbers may change over time):

9. nucleotide level C reports

* Output

Relative to the project directory, the following files will be generated:

c_methyl_report/<SAMPLENAME>/cytosine-nucleotide-level-report.txt
c_methyl_report/<SAMPLENAME>/cytosine-tile-level-report.txt

Scripts
--------

* bismark_nuc-level_methylation_run.pl - Set up environment and launch jobs.

* bismark_nuc-level_methylation.pl - Generate nucelotide level reports of genomic cytosine positions and methylation status.

