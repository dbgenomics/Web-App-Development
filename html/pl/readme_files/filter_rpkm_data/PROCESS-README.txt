Filter RPKM Data
Author: Nick Bild
Date: 2016-05-03
Version 1.0: Initial development.

Description
--------

The Filter RPKM Data pipeline filters data tables and replaces low values according to user input.

Script relationships:

filter_merged_counts.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

2. filter RPKM data

The following questions will be asked:

- Enter the merged file to be filtered (including the full path, e.g.: /path/to/file.txt)
- Enter a comma-delimited list of threshold files to include.
e.g.: /path/to/project1/easyrnaseq/threshold.txt,/path/to/project2/easyrnaseq/threshold.txt,/path/to/project3/easyrnaseq/threshold.txt
Files: thresholds_merged.txt
- Which row contains the values used to calculate the replacement value (detection threshold, usually RPKM ~ 10 reads, header row = 1)?
- Which row is to be used as the threshold value for filtering (reliable quantification threshold, usually RPKM ~ 50 reads, header row = 1)?
- Specify the percentage of samples that must pass filter to be retained (e.g. 25, leave blank to specify 1+ samples):
- How many annotation columns does the data contain?

The input data file is expected to be a tab-delimited text file, with annotation columns followed by data columns.

The threshold file(s) must be a tab-delimited text file that contains a header row (1st row) with sample names matching the sample names in the data files.  When specifying row numbers for the detection threshold and reliable quantification threshold, use 1-based counting, i.e. the header row would be entered as "1".  All threshold files specified must have the same row structure.

In order to pass filter, a gene must contain 1+ samples (or have >= user-specified % of samples) that are >= the reliable quantification threshold.

Any value that is <= the 99.9% of its detection threshold is replaced with the replacement value (mean of the detection threshold across all samples).

Output will be named <inputfile>.filtered.txt

* Alternatively, to run the pipeline manually:

cd to the project directory, then run:

/home/act/software/nickbild/filter_merged_counts.pl

The workflow matches the pipeline version after this point.

Scripts
--------

* filter_merged_counts.pl - Filter and replace values in merged RPKM data file.

