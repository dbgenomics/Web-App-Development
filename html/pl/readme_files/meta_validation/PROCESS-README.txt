Metagenome Validation Pipeline
Author: Nick Bild
Date: 2016-07-14
Version 1.0: Initial development.

Description
--------

The Metagenome Validation Pipeline generates validation reports for metagenomics experiments.

Script relationships:

form.html
|
-- api.cgi (calls validation_run.pl remotely)
|
-- status.cgi

validation_run.pl
|
-- file_compare.pl
|
-- get_gen_len.pl
|
-- raw_data_check.pl
|
-- igv_png.pl
|  |
|  -- igv.py
|
-- report.pl

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.  Python v2.7 is required.

IGV must be installed and running on 192.168.0.18 to generate genome browser snapshot images.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/meta_validation_pipeline.

Web API is installed on yonggan (192.168.0.16) in /home/yonggan/www/pl/meta_validation.

Usage Instructions
--------

* The pipeline is available via ORB Intranet (http://192.168.0.16/):

Sequencing -> Metagenome Validation

The following questions will be asked:

- Enter a comma-delimited list of genes to validate (no spaces; leave blank to select the first 5 genes in the datafile)

This is used to specify the genes that you wish to include in the validation reports.  If no genes are specified, the first 5 genes in the datafile will be selected.

- Enter the full path to the project directory on marburg

This is needed to located BAM files.

- Select the IGV genome to use:

For IGV image generation.

- Enter an RPKM file: 

final/rpm.merged.annotated.txt from metagenome project folder.

- Enter an RPM file:

final/rpm.merged.annotated.txt from metagenome project folder.

- Enter a raw count file:

final/combined.annotated.txt from metagenome project folder.

- Select sampleinfo file: 

Sample names must be in the first column.

- Select total counts file: 

Must be a tab-delimited total_counts.txt file, in which the 1st row must be sample names, and the 2nd must be the total counts.

- Select GTF annotation file:

Choose the file corresponfing to the genome version and annotation version used in the data analysis. 

Output:

Output will be written in a "validation" subdirectory of the "webdata" output folder.  These files will be present:

* file_compare.txt

- Compares values from input files for genes of interest. 

The following columns will be present:
Gene			-- Gene ID
Sample			-- Sample Name
RPKM			-- RPKM value
RPM			-- RPM value
Raw			-- Raw count value

* raw_data_check.txt

- RAW DATA CHECK Filter the GTF file to generate a gene-specific GTF.  Remove redundant regions in GTF.  Select 3 BAM files containing the lowest, medium, and highest count for the gene.  Count alignments to the gene with bedtools.

The file format is:
Gene	Sample 1	Sample2	...	SampleN
GeneID	sample1count	sample2count	...	sampleNcount

* <geneID>.png

- GRAPHICAL CONFIRMATION Generate .png files showing the alignment of reads in 3 BAM files to one specific gene.

A separate PNG file is generated for each gene being validated.

Note that IGV must be running on 192.168.0.18 for this step to work correctly.

* settings.txt

Lists user-specified settings and files specific to the analysis.

* A summary HTML report will also be generated.

Scripts
--------

* validation_run.pl - Main controller script the collects user input and launches all subsequent steps.

* file_compare.pl - Runs file comparison step.

* raw_data_check.pl - Runs raw data check step.

* get_gen_len.pl - Get lengths of genes of interest.

* igv_png.pl - Runs graphical confirmation step.

* igv.py - API for interacting with IGV remotely.

* form.html - Collect user input for web app.

* api.cgi - Upload and prepare data for processing.  Call validation_run.pl remotely.

* status.cgi - Monitor progress of remote job, and present results to user.

* report.pl - Generate HTML summary report.

