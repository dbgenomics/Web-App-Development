Dunnett's Test
Author: Nick Bild
Date: 2016-09-02
Version 1.0: Initial development.
2017-10-30 NAB
Fold changes to be calculated as the mean of the untransformed values for group X divided by the mean of the untransformed values for group Y.
Ask if thresholds are log transformed, and untransform values if needed.

Description
--------------------------------------------------------------------------------

The Dunnett's Test statanalysis application will will collect user input to perform Dunnett's test, as specified by the sampleinfo file.

Script relationships:

dunnetts_test.pl
|
-- run_dunnetts_test.R

Dependencies
--------------------------------------------------------------------------------

Perl v5 is required. R 3.2.2 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/ and /home/act/software/ogden/.

Usage Instructions
--------------------------------------------------------------------------------

* The pipeline is available as part of statanalysis (note that step numbers may change over time):

12. Dunnett's test

The following questions will be asked:

* Enter the data file (including full path):

Tab-delimited file with expression data.  Sample names in header row must match
sample names in sampleinfo file. The data file can contain extra samples. Only
samples found in both the data file and the sample information file will be
used for analysis. The data file may contain annotation columns. Annotation
columns in columns 2 to 8 will be kept in the results, if they are present.

* Enter the threshold file (including full path):

Tab-delimited with a header row and a single threshold row. The header row must
have the sample names and the sample names must match those in column 1 of the
sampleinfo file and the header row of data file. The threshold file may contain
extra samples -- only samples in the sample information file will be used.

* Which log base is the data file already in (e.g.: 2. Leave blank if not log transformed.)?

Data will be log2 transformed for analyses.  Fold changes will be calculated with untransformed group averages.

* Which log base is the thresholds file already in (e.g.: 2. Leave blank if not log transformed.)?

This will be used (if necessary) to untransform thresholds for used in fold change calculation (for "NA").

Sampleinfo
--------------------------------------------------------------------------------

Tab-delimited file containing sample group information.

Column 1 of the sample information file must contain the sample names that
appear in the header row of the data file and also the header row of the
threshold file. 

Column 6 must have the single factor and there must be a 'Group
Order' column that contains numbers starting at 1 corresponding to the order of
the levels in the single factor for the ANOVA. 

The 'Group Order' column can appear in any column of the sampleinfo file,
including column 6 (in which case the Group Order will be the group). Obviously
each group should correspond to one and only one Group Order (but the script
will check this).

Additional columns may be present in the sample information file; the only
columns used for analysis are columns 1 and 6 and the column named "Group Order".

The Group Order column is used to sort the groups in ascending order so that
the control group is first. To achieve this, it should contain a 1 for the
control group in each analysis and then the second group would be 2, and so.

For example, the sample info file shown below:

Sample ID	Col2	Col3	Col4	Col5	Group	Group Order
HYH0001  	-	-	-	-	G1	1
HYH0002  	-	-	-	-	G1	1
HYH0003  	-	-	-	-	G8	2
HYH0004  	-	-	-	-	G8	2
HYH0005  	-	-	-	-	G15	3
HYH0006  	-	-	-	-	G15	3

would compare G8 vs. G1 and G15 vs. G1.

Output
--------------------------------------------------------------------------------

<DATAFILE>.dunnett.txt			-- Data file, with columns added for P values, FDRs, and fold changes from Dunnett's tests.

Scripts
--------------------------------------------------------------------------------

* dunnetts_test.pl - Collect user input and call run_dunnetts_test.R.

* run_dunnetts_test.R - Perform Dunnett's tests as specified in the sampleinfo file.

