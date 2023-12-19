Circadian Analysis with JTK_CYCLE
Author: Nick Bild
Date: 2016-04-21
Version 1.0: Initial development.

Description
--------

The Circadian Analysis with JTK_CYCLE pipeline prepares tab-delimited text files for use with JTK_CYCLE.  JTK_CYCLE is then run on each group of samples (as specified in the sampleinfo file.

Script relationships:

jtk_run.pl
|
-- JTK_CYCLEv3.1.R

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/jtk_cycle.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

11. circadian analysis with JTK_CYCLE

* Alternatively, to run the pipeline manually:

cd to an appropriate working directory.

Run:
/home/act/software/nickbild/jtk_cycle/jtk_run.pl [SAMPLEINFO]

The following questions will be asked:

* Specify the data file (including the full path):
e.g.: /path/to/easyRNASeq_Anno_Martinez-Nunez_genes_raw.txt

Output will be placed in a directory named "jtk_cycle" in the current working directory.  An additional directory will be created for each project.  Output will consist of:

JTK.<project>.txt			- JTK_CYCLE output.
JTK.<project>.rda			- JTK_CYCLE output.
<datafile>.<project>.anno.txt		- Annotation file for input into JTK_CYCLE.
<datafile>.<project>.txt		- Data for input into JTK_CYCLE.
<project>.R				- R file for running JTK_CYCLE.
<project>.Rout				- R output.

Sampleinfo File:

Column 1 must match the data headers in the data file.  The last column must be named "ZT" and contain the Zeitbeger times for each sample.  Column 6 through the column before ZT will be used to create the groups.

Scripts
--------

* jtk_run.pl - Prepare input for JTK_CYCLE, JTK_CYCLE R script, and run JTK_CYCLE on each group, as specified in the sampleinfo file.

* JTK_CYCLEv3.1.R - JTK_CYCLE v3.1 R source.

