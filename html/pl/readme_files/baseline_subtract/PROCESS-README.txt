Baseline Subtraction Pipeline
Author: Nick Bild
Date: 2016-02-03
Version 1.0: Initial development.
Version 1.1: 2016-05-04 NAB
Generalize script so that it can handle easyRNASeq or microarray data without asking question.
Reverse logic on log2 question.  Instaed of "do you want to log2 transform data?" ask "Is the data log2 transformed?".
Check for <=0 values if data not already log transformed.

Description
--------

The Baseline Subtraction Pipeline will subtract user-specified baseline samples from every other data point for the same subject.

Script relationships:

baseline_subtract.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

4. baseline subtract easyRNASeq or microarray

The following questions will be asked:

Is the data log2 transformed? Y/N:
 e.g. N
How many annotation columns exist in the input? Number:
 e.g. 8
Enter the name of the data file: File:
 e.g. /path/to/datafile.txt

The input must be a tab-delimited text file, with annotation columns followed by data columns.

The filtered file will be a renamed version of the input file, with a ".baseline.txt" extension.

Sampleinfo File:

sampleinfo file must contain subject in column 9 and baseline flag in column 10.
Example:
#Sequencing Data ID    Sample Name     ORB Enriched DNA Library ID     PaxGene Barcode Cohort  Dose_mg_per_kg  Day     Treat   Subject Baseline
SL126850       3507-CN-0001    CM4612601       A012L8XE1       1       33      D1      Pre     102-101 Yes
SL126851       3507-CN-0002    CM4612602       A012L8XE2       1       33      D1      2hr     102-101 No
SL126852       3507-CN-0003    CM4612603       A012L6I20       1       33      D1      Pre     101-101 Yes
SL126853       3507-CN-0004    CM4612604       A012L6I21       1       33      D1      2hr     101-101 No

* Alternatively, to run the pipeline manually:

cd to the project directory, then run:

/home/act/software/nickbild/baseline_subtract.pl sampleinfo.txt

The workflow matches the pipeline version after this point.

Scripts
--------

* baseline_subtract.pl - Subtracts user-specified baseline samples from every other data point for the same subject.

