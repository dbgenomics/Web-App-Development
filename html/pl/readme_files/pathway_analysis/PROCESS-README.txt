Pathway Analysis Pipeline
Author: Nick Bild
Date: 2016-03-09
Version 1.0: Initial development.
2011_ORB_Company_Files/ORB-Computational-Methods/2016-03-08_Pathway_Analysis_Pipeline_Description.txt
Update: 2016-03-15
2011_ORB_Company_Files/ORB-Computational-Methods/2016-03-14-Pathway-Analysis-Software-Corrections.docx
UPDATE 2016-04-14: Nick Bild
Version 1.1: Add web support.
Allow for multiple "P Value Column" values in pathway config file.
UPDATE 2016-05-04: Nick Bild
Split "Settings Files" into a separate archive.
Update pathway_analysis_add_stats.pl to pull p-values and fold changes in for other id types (Entrez, Gene Symbol).
UPDATE 2016-05-10: Nick Bild
Add fix for situtations where WebGestalt maps 0 IDs.
Add "Report Subtitle" and "Report Name Prefix" fields.
UPDATE 2016-08-30 NAB
Add support for human orthologs with Pathway Commons (PC only supports human genes).

Description
--------

The Pathway Analysis pipeline performs a pathway analysis via WebGestalt (http://bioinfo.vanderbilt.edu/webgestalt) on gene lists derived from a raw data file containing gene IDs, p-values, and fold changes.  Criteria for creating the gene lists are supplied by the pathway config file.  An HTML report for all analyses is provided.

Script relationships:

WEB:

form.html
|
-- api.cgi
   |
   pathway_analysis_run.pl
   |
   -- runwebgestalt.R
   |
   -- pathway_analysis_report.pl
   |  |
   |  -- pathway_analysis_datatables_merge_all_input.pl
   |  |  |
   |  |  -- jquery-2.2.1.min.js
   |  |  |
   |  |  -- datatables.min.js
   |  |  |
   |  |  -- datatables.min.css
   |  |
   |  -- pathway_analysis_add_stats.pl
   |  |  |
   |  |  -- jquery-2.2.1.min.js
   |  |  |
   |  |  -- datatables.min.js
   |  |  |
   |  |  -- datatables.min.css
   |  |
   |  -- parse_webgestalt_results.R
   |
   -- status.cgi

COMMAND LINE:

pathway_analysis_run.pl
|
-- runwebgestalt.R
|
-- pathway_analysis_report.pl
   |
   -- pathway_analysis_datatables_merge_all_input.pl
   |  |
   |  -- jquery-2.2.1.min.js
   |  |
   |  -- datatables.min.js
   |  |
   |  -- datatables.min.css
   |
   -- pathway_analysis_add_stats.pl
   |  |
   |  -- jquery-2.2.1.min.js
   |  |
   |  -- datatables.min.js
   |  |
   |  -- datatables.min.css
   |
   -- parse_webgestalt_results.R

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.

Required R modules:
rvest
xml2
httr
magrittr
dplyr
reshape2
docopt
XML

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/pathway_analysis.

Usage Instructions
--------

* The pipeline is also available as part of the ORB Intranet:

http://192.168.0.16/ -> Pathway -> Web Gestalt Analysis

The following questions will be asked:

* Species?
 e.g.: Human

* Which column contains the gene identifier?
 e.g.: 1

* What is the gene identifier type? 
 e.g.: Ensembl Gene ID

* Specify the minimum number of genes for a category:
 e.g.: 2

* Specify the significance level for the enrichment analysis. Top 10 option always identifies the 10 pathways with the most significant p values.
 e.g.: .1

* Report Subtitle:
Subtitle shown in HTML report.

* Report Name Prefix:
Prefix for final reports.

* Reference Set File Name:
This name will be used to rename the reference file as <RefSetFileName>.txt
When there is also a Brief Description in the Config file, this name will be added to the beginning of the Brief Description to create the geneset file name.
NOTE According to WebGestalt, the file can only contain characters, numbers, underscores, dashes.
Do not enter the '.txt' suffix. 

* Select data file:
The data file is expected to have annotation columns first, followed by data columns. The
first row in the data file must be a header row.

* Select pathway config file:
See web app for full description.

Pathway Config File:

This is a tab-delimited text files that specifies the criteria used to select genes for a gene set, which will be used for pathway analysis.  It should consist of a header row followed by one or more configuration rows. Here is an example that specifies two criteria:

P Value Column	P Value Cutoff	Fold Change Column	Fold Change Cutoff Up	Fold Change Cutoff Down	Description	Brief Criteria Description
P.Dose.Time	0.05	FoldChanges_(D7-D1)_at_fixed_(Pre_33)	1.5	1.5	Tukey P value < 0.05 and fold change > 1.7 up/down for D7 vs. D1 (Pre 33 mg/kg)
P.Dose.Time	0.05	FoldChanges_(D7-D1)_at_fixed_(Pre_67)	1.5	1.5	Tukey P value < 0.05 and fold change > 1.7 up/down for D7 vs. D1 (Pre 67 mg/kg)

Multiple columns may be specified in "P Value Column", separated by "~~". Accordingly, these column names must not contain "~~". The minimum data value from all specified columns will be found, and that minimum value will be compared to the "P Value Cutoff" during filtering. The column names refer to column names defined in the raw data file. For each row in the config file, a separate gene list will be created, and a pathway analysis will be run on each gene list. If a description is not specified, it will be defined as:

[P Value Column]_[P Value Cutoff]_[Fold Change Column]_[Fold Change Cutoff Up]_[Fold Change Cutoff Down]

See "/home/act/software/documentation/pathway_analysis/pathway_config_template.cfg" for a complete example pathway config file.

Output:

The user will be presented with zip files containing the report and supporting files, a separate settings zip, and a link to immediately view the report.

Orthologs:

Human orthologs will be determined and supplied to WebGestalt where the selected species is not supported.  When orthologs are used, the affected columns will be labeled accordingly to indicate the substitution.

Scripts
--------

* pathway_analysis_run.pl - Creates filtered gene lists and runs the pathway analyses.

* runwebgestalt.R - Script developed by Kevin Ogden to call the WebGestalt software via HTTP post.

* pathway_analysis_report.pl- Generates an HTML report for all analyses conducted.

* pathway_analysis_datatables_merge_all_input.pl - Generates a DataTables HTML version of the gene set inputs.

* pathway_analysis_add_stats.pl - Add statistics from the raw data file to the WebGestalt output.

* parse_webgestalt_results.R - Script developed by Kevin Ogden to parse WebGestalt HTML output into text files.

* jquery-2.2.1.min.js - jQuery source (http://jquery.com/).  Required by DataTables.

* datatables.min.js - DataTables source (http://datatables.net/).  Makes paginated, searchable HTML tables.

* datatables.min.css - DataTables style sheets.  Control DataTables appearance.

* form.html - Collect user input.

* api.cgi - Launch marburg job from web.

* status.cgi - Check status of marburg job and allow for download of results on web.

