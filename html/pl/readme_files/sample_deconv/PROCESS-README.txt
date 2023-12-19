Deconvolution of Tissue or Cell-Type Composition of RNA Sequencing Samples
Author: Nick Bild
Date: 2017-06-05
Version 1.0: Initial development.

Description
--------

The Deconvolution of Tissue or Cell-Type Composition of RNA Sequencing Samples app will accept expression data and a cell or tissue type expression profile, and provide an estimate of the proportion of each tissue or cell-type present in each input sample.

Script relationships:

form.html
|
-- api.cgi
   |
   -- deconvolution_run.pl
   |
   -- status.cgi

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.

Required R modules:
DeconRNASeq

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/deconvolution and yonggan (192.168.0.16) at /home/yonggan/www/pl/sample_deconv.

Usage Instructions
--------

* The pipeline is available as part of the ORB Intranet:

http://192.168.0.16/ -> Statistics -> Sample Deconvolution

The following questions will be asked:

* Which column contains the gene identifier (Ensembl IDs expected)?

This is the column number in the data file that contains the Ensembl gene ID.

* If you wish to include only certain tissue/cell types, enter them here (comma-separated, must be identical to values in signatures file).

Entering tissue/cell types here will focus the analysis on just those entries from the gene signatures reference file.  Leave this blank to use the entire gene signatures reference file.

* Select a gene expression signatures reference file:

Select the appropriate signature file for the species of interest, and tissue/cell type.

* Select expression data file:

The first row in the data file must be a header row, and sample names must match sampleinfo file.
Expression values should be normalized in some way (e.g.: RPKM).

* Select sampleinfo file:

Sample names must be in the first column.

Output:

<DATAFILE>.deconvoluted.txt				-- Proportion of each tissue or cell-type present in each input sample.
settings.txt						-- A list of user-selected files and parameters used to conduct the analysis.

Scripts
--------

* deconvolution_run.pl - Prepare data, run DeconRNASeq, and prepare output.

* form.html - Collect user input.

* api.cgi - Launch marburg job from web.

* status.cgi - Check status of marburg job and allow for download of results on web.

