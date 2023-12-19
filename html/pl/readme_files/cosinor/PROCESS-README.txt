Cosinor Circadian Analysis Pipeline
Author: Nick Bild
Date: 2016-05-09
Version 1.0: Initial development.
Date: 2016-06-17 NAB
Give user option to treat numeric covariates as continuous variables.
Set period length to 24 hours.
Rename output columns to contain covariate names.
Report p-value for test of covariate.
Add plots of fitted curves, and group average RPKMs +/- standard error.
Run each cosinor job (gene) on a seperate cluster job.
Date: 2016-07-07 NAB
Add covariate labels to output headers.
Add "--no-save" to R CMD BATCH.
Remove confidence interval columns from final output.
Add test for acrophase.
Rename columns.
Remove plotting capabilities.
Reorganize output folder.

Description
--------

The Cosinor Circadian Analysis Pipeline will prepare gene expression data from microarrays or RNA-seq to identify genes whose expression cycles within a circadian fashion.

Script relationships:

cosinor_run.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/cosinor.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

14. circadian anaylsis using the cosinor method

The following questions will be asked:

Specify the data file (including the full path):
 e.g.: easyRNASeq_Filter_Circadian_Rhythm_genes_rpkm.txt.small
Do you want to treat numeric covariates as continuous variables (Y/N)?
 e.g.: N

The input must be a tab-delimited text file, with annotation columns followed by data columns.

Output will be placed in the "cosinor" directory, under the current working directory.  With 0 or 1 co-variates, the output file will be named:

<datafile>.cosinar.txt

In the case of 2 co-variates, the data will be split according the the 1st co-variate.  The 2nd co-variate will be included in the cosinor analysis.  Files will be named:

<datafile>.cosinar.<covariate1name>.txt

A maximum of 2 co-variates are supported.

Sampleinfo File:

The sample information must have a column labeled “ZT” (for Zeitgeber time), which must occur after the 5th column and be the last column. Any co-variates, for example, Diet or Drug, must come after the 5th column and before the “ZT” Column. If there are two covariates, data is split by the values of the first factor.

Here is an example with 2 co-variates:

#Sequencing Data ID	Sample Name	ORB Enriched Library ID 	Label on Tube	Project	Diet	Drug	ZT
SL150613	3927-CN-0001	CC51108001	WZAF-009-15 #1 Gr 1 Vena Cava 0hr	Circadian_Rhythm	C57	Vehicle	0
SL150614	3927-CN-0002	CC51108002	WZAF-009-15 #2 Gr 1 Vena Cava 0hr	Circadian_Rhythm	C57	Vehicle	0
SL150615	3927-CN-0003	CC51108003	WZAF-009-15 #6 Gr 2 Vena Cava 0hr	Circadian_Rhythm	C57	ZGN440	0
SL150616	3927-CN-0004	CC51108004	WZAF-009-15 #7 Gr 2 Vena Cava 0hr	Circadian_Rhythm	C57	ZGN440	0
SL150617	3927-CN-0005	CC51108005	WZAF-009-15 #11 Gr 3 Vena Cava 4hr	Circadian_Rhythm	C57	Vehicle	4
SL150618	3927-CN-0006	CC51108006	WZAF-009-15 #12 Gr 3 Vena Cava 4hr	Circadian_Rhythm	C57	Vehicle	4
SL150619	3927-CN-0007	CC51108007	WZAF-009-15 #13 Gr 3 Vena Cava 4hr	Circadian_Rhythm	C57	Vehicle	4
SL150620	3927-CN-0008	CC51108065	WZAF-009-15 #19 Gr 4 Vena Cava 4hr	Circadian_Rhythm	C57	ZGN440	4
SL150621	3927-CN-0009	CC51108009	WZAF-009-15 #17 Gr 4 Vena Cava 4hr	Circadian_Rhythm	C57	ZGN440	4
SL150622	3927-CN-0010	CC51108010	WZAF-009-15 #18 Gr 4 Vena Cava 4hr	Circadian_Rhythm	C57	ZGN440	4

* Alternatively, to run the pipeline manually:

cd to the project directory, then run:

/home/act/software/nickbild/cosinor/cosinor_run.pl sampleinfo.txt

The workflow matches the pipeline version after this point.

Scripts
--------

* cosinor_run.pl - Prepares data, runs cosinor, and merges cosinor results with input data.

