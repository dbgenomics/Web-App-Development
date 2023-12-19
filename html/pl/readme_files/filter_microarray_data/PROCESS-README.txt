Filter Microarray Data Pipeline
Author: Nick Bild
Date: 2016-02-03
Version 1.0: Initial development.

Description
--------

The Filter Microarray Data Pipeline will filter microarray data.  The user will be prompted for threshold values, and the percentage of samples that must be >= to the thresholds to be retained.

Script relationships:

filter_merged_counts_micro.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

3. filter microarray data

* Microarray data filtering is also available via: http://192.168.0.16/home.cgi (Programs -> microArray -> Filtering).

The following questions will be asked:

Enter threshold file to use. File:
 e.g.: /path/to/thresholdfile.txt
Which row in the threshold file contains the threshold value. Number:
 e.g.: 6
Percentage of samples in which a probe must be >= the detection limit in order to be retained (e.g. 25)? Number:
 e.g.: 25
How many annotation columns exist in the input? Number:
 e.g.: 8
Enter the name of the data file: File:
 e.g.: /path/to/datafile

Threshold data:

For microarray data, the threshold file is expected to be output from the microarray webapp on 192.168.0.16
It should have at least two rows: the first row should start with `#Category' and contain the sample names,
and the second row would have the threshold values. The rows are numbered starting at 1 -- the first row
in the file is row 1.

The input data file is expected to be a tab-delimited text file, with annotation columns followed by data columns.

The filtered output will be a renamed version of the input file, with a "_filtered.txt" extension.

* Alternatively, to run the pipeline manually:

cd to the project directory, then run:

/home/act/software/nickbild/filter_merged_counts_micro.pl

The workflow matches the pipeline version after this point.


Scripts
--------

* filter_merged_counts_micro.pl - Filter externally merged microarray data. User will be prompted for threshold values, and the percentage of samples that must be >= to the thresholds to be retained.

