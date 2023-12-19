Principal Components Analysis Pipeline
Author: Nick Bild
Date: 2016-02-19
Version 1.0: Initial development.
Date: 2016-03-30
Version 2.0: Webify and add HTML report.
Date: 2016-05-19
Update documentation to include Data Analysis Apps.
Date: 2016-05-26 NAB
Replaced the “User Project Description” option with two options -- a “Report Subtitle” and a “Report Name Prefix”.
Formatted the number of genes with a thousands-separator
Provideed a sample info file for download
Name the reports as REPORTPREFIX_PCA_Report.html
Updated the pca.R script backend to the one at /home/act/software/ogden/pca.R
Added an option to use colors for the sample names.
Provided an option for whether the group names in the “Visualization of PCs” plots appears in the plot or as a legend.

Description
--------

The Principal Components Analysis pipeline performs a PCA on supplied raw data.  PCA is conducted via R script developed by Kevin Ogden.  An HTML report of the results is generated.

Script relationships:

form.html
|
-- run_program.cgi
   |
   -- pca.pl
      |
      -- pca.R
      |
      -- pca_html.pl
         |
         -- pca_include.js
         |
         -- pca_html_detailed_results.pl
            |
            -- datatables.min.css
            |
            -- datatables.min.js
            |
            -- jquery-2.2.1.min.js

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  The following R libraries are required:

docopt
magrittr
ggplot2
RColorBrewer
reshape2
dplyr

Software installed on yonggan-Precision-WorkStation-T5400 (192.168.0.16) in /home/yonggan/www/pl/pca.

For Data Analysis Apps, software is also installed on fileserver (10.1.10.104) in /home/nick.

Usage Instructions
--------

* The pipline is available as part of the ORB intranet, and this is the only method of running the pipeline.

http://192.168.0.16/

Software -> Statistics -> Principal Components Analysis

The following questions will be asked:

- How many principal components would you like returned (e.g.: 3)?
- If the data is log transformed, what is the base (e.g.: 2)?
- Enter fold-change criteria for clusters (e.g.: 2):
- Enter correlation criteria for clusters (e.g.: 0.7):
- Do you want to filter the data? If yes, enter the columns to filter (comma-separated list, e.g.: 9,10,11):
- If filtering, what is your filtering cutoff value (e.g. 0.05)? 1+ genes in filter columns must be < this value to be retained.
- Which column would you like to use to shade the plots? (e.g.: 2)
- Do you want to use colors for the sample names?  (e.g.: Y)
- Do you want to show a legend for Visualization of PCs instead of labeling data points? (e.g.: Y)
- Enter the width of the column projection plots:  (e.g.: 1350)
- Enter the height of the column projection plots:  (e.g.: 1350)
- Enter the width of the cluster plots:  (e.g.: 1800)
- Enter the height of the cluster plots:  (e.g.: 1800)

For the next set of questions, users may select a choice from the dropdown, or enter their own value.  These values will modify the HTML report by being inserted into the proper locations:

- Feature type?
- Data type?
- Species?

To modify the description at the top of the text, this question is asked:

- Criteria Text
- Report Subtitle

A prefix for output folders and files is specified by:

- Report Name Prefix

The next question will force PCA to be done on individual samples even when the sample info file is set to group samples.  Column 4 alone will be used to rename samples in individual sample mode.

- Would you like to force individual PCA mode? This is useful if the sampleinfo is set up for group PCA, but you want to run an individual PCA.

To get the necessary input files:

- Select data file:
	User may browse local computer for a data file, or specify the absolute path to the file on marburg.

- Select sampleinfo file:
	User may browse local computer for a sampleinfo file, specify the absolute path to the file on marburg, or paste the data into the textbox.

The sampleinfo file must be a tab-delimited text file, and:
-  Samples are renamed using the values in columns 6, 7, etc. up until the
   last column, which should be named "Plot Order". Values from these
   columns are concatenated with an underscore separating them.
-  If the new sample names are all unique, then PCA will be done on
   individual samples with these new names.
-  If the new samples are not unique, then PCA will be done on the group
   averages.  All samples with the same name will be averaged together.
-  The "Plot Order" column must come last and will determine the plotting
   order for the Sample-specific PC Plots. It should consist of numbers
   starting at 1 and increasing by 1 until at most the number of samples
   in the data file. The data columns in the data file will be reordered
   according the order in the Plot Order column.
-  If the answer to "Would you like to force individual PCA mode?" question is "Y",
   then PCA will be done by individual samples, regardless of how the sample
   info is set up.  With this option, samples are renamed with the value in
   Column 4 of the sample info -- Columns 6, 7, ... are *not* used.

After clicking "next", the user will be presented with links to download an archive containing the HTML report and associated files for offline viewing, as well as a link to view the HTML report immediately.  settings.txt lists user-specified settings and files specific to the analysis.

Scripts
--------

* form.html - Collect user input.

* run_program.cgi - Parse user input, upload files, and launch pca.pl.

* pca.pl - Prepare and filter data for pca.R.

* pca.R - Script to run PCA, developed by Kevin Ogden.

* pca_html.pl - Generate HTML report of PCA results.

* pca_include.js - Javascript to include in HTML.

* pca_html_detailed_results.pl - Builds a DataTable of detailed results for viewing as a separate HTML page.

* datatables.min.css - DataTables style files.

* datatables.min.js - DataTables javascript files.

* jquery-2.2.1.min.js - JQuery -- required by DataTables.

