Hierarchical Clustering Pipeline
Author: Nick Bild
Date: 2016-02-22
Version 1.0: Initial development.
Update: 2016-03-30
Version 2.0: Convert to web app.
Update: 2016-05-19 Nick Bild
Update documentation to include Data Analysis Apps.
Version 2.1
Update: 2016-05-26 NAB
1. Format the number of genes with a thousands-separator
2. Add a link for Cluster 3.0 -- http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm
3. Revise the phrase "Adjusted data by median centering <FEATURES>" to "For each <FEATURE>, the median across all samples was subtracted from each value."
4. Change the phrase "Performed clustering of genes and samples using centered correlation as distance measure and average linkage as method." to "Genes and samples were clustered using centered correlation as the similarity measure and average linkage as the clustering method."
5. Add this citation for Java Treeview
Saldanha AJ (2004) Java Treeview – extensible visualization of microarray data. Bioinformatics 20(17), 3246-48.
6. Add a link to the SourceForge download page (http://jtreeview.sourceforge.net/)
7. Replace the “User Project Description” option with two options -- a “Report Subtitle” and a “Report Name Prefix” (similar to the input for the Pathway App).
8. Name the cdt file as REPORTPREFIX_FEATURE_DATATYPE.cdt e.g. 2016-05-04 Koenig_mRNA-Seq_genes_rpkms.cdt
9. Allow changing the contrast after the clustering completes without re-clustering (simply re-generate the image)
10. Output should contain an about.txt file with a time stamp and the setting entered.

Description
--------

The Hierarchical Clustering pipeline filters and clusters raw data.

Script relationships:

form.html
|
-- clustering_api.cgi
   |
   -- clustering_web.pl
   |
   -- status.cgi

clustering.pl

The general method of interaction between web applications and marburg is described in the "webapp_marburg_execution" documentation folder.

Dependencies
--------

Perl v5 is required.

Cluster 3.0 is required (http://bonsai.ims.u-tokyo.ac.jp/~mdehoon/software/cluster).  It should be installed in /opt/.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild and yonggan-Precision-WorkStation-T5400 (192.168.0.16) in /home/yonggan/www/pl/hierarchical_clustering.

For Data Analysis Apps, software is also installed on fileserver (10.1.10.104) in /home/nick.

Usage Instructions
--------

* The preferred method of using the pipeline is via the ORB Intranet:

http://192.168.0.16/
Software -> Statistics -> Hierarchical Clustering

The following questions will be asked:

- Which columns in the sampleinfo file should be combined to name the samples (comma-separated list, e.g.: 6,7,8)?
- Which annotation columns should be combined to create a new gene id (comma-separated list, e.g.: 1,6,8)?
- Is the data log transformed?
  e.g. N
- Do you want to cluster by samples?
  e.g. Y
- Select a contrast level for TreeView image generation:
  e.g. 3
- Do you want to filter the data? If yes, enter the columns to filter (comma-separated list, e.g.: 9,10,11):
- If filtering, what is your filtering cutoff value (e.g. 0.05)? 1+ genes in filter columns must be < this value to be retained.
- To filter by threshold values, paste the thresholds file in the text box below:
  e.g.:
  Sample	samplename1	samplename2	...	samplenameN
  Threshold	val1	val2	...	valN
- If filtering by threshold values, what percentage of samples for a gene must be >= the detection limit in order to be retained (e.g. 25)?
- Description of filtering criteria:     
  e.g.: minimum P value for ANOVA testing effect of animal age
- Report Subtitle
  e.g.: Subtitle of Report
- Report Name Prefix
  e.g.: projectname
- Feature type?     
  e.g.: genes
- Data Type?
  e.g. RPKMs
- Select data file:
  This can be selected from your local computer, or by supplying an absolute path to the file on marburg.
- Select sampleinfo file:
  This can be selected from your local computer, by supplying an absolute path to the file on marburg, or by pasting data into the textbox.

The clustering job is submitted to marburg.  A status screen will be displayed, and it will auto-refresh and alert the user when results are ready.  The filtered data file, the cluster 3.0 output (*.cdt, *.atr, *.gtr), a TreeView PNG file (web version only), an HTML report (web version only), and a .zip file of all results (web version only) will all be available for download.  settings.txt lists user-specified settings and files specific to the analysis.

* The pipline is available as part of the tophatanalysis2 pipeline (note that step numbers may change over time):

40. Hierarchical Clustering

* Alternatively, to run the pipeline manually:

cd /home/act/software/nickbild

./clustering.pl sampleinfo

The following questions will be asked:

- Specify the data file (including the full path):
e.g.: /home/act/software/nickbild/datafile.txt
- Which columns in the sampleinfo file should be combined to name the samples (comma-separated list, e.g.: 6,7,8)?
e.g.: 6,7,8
- Which annotation columns should be combined to create a new gene id (comma-separated list, e.g.: 1,6,8)?
e.g.: 1,6,8
- Is the data log transformed (Y/N)?
e.g.: N
- Do you want to filter the data?  If yes, enter the columns to filter (comma-separated list, e.g.: 9,10,11):
e.g.: 9,10,11
- What is your filtering cutoff value (e.g. 0.05)? 1+ genes in filter columns must be < this value to be retained.
e.g.: 0.05
- In which column does your data begin?
e.g.: 9

Scripts
--------

* form.html - Collects parameters from user.

* clustering_api.cgi - Sets up the environment, transfers files, and starts a clustering job on marburg.

* clustering_web.pl - On marburg.  Performs the clustering.  Non-interactive version of clustering.pl for web use.

* status.cgi - Monitors progress of job on marburg, and presents results to user.

* clustering.pl - This script will transform raw data into the format required by Cluster 3.0, and will set the appropriate command line parameters based on user input.  This is used for the command line version of the pipeline only, and is no longer being updated.  It should not be used.

