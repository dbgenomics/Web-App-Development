Bisulfite Coverage Report
Author: Nick Bild
Date: 2016-07-25
Version 1.0: Initial development.

Description
--------

Bisulfite Coverage Report generates coverage statistics and images and prepares a report.

Script relationships:

bisulfite_coverage_report.pl
|
-- bisulfite_cpg_density.pl
|
-- bisulfite_cpg_enrichment.pl
|
-- igv_png_bisulfite.pl
|  |
|  -- igv_bisulfite.py
|
-- bisulfite_coverage_html.pl

Dependencies
--------

Perl v5 is required.  Python 2.7 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* Bisulfite Coverage Report is available via the bisulfiteseq pipeline (note that step numbers may change over time):

7. coverage report

The following questions will be asked:

- Selections for the following keys from oap_database.txt will need to be made:

IGV			-- IGV genome.
CPG_GENOME		-- CpG statistics for an unconverted reference genome.
GTF			-- GTF annotation.

- Enter a comma-delimited list of genes to generate IGV snapsots for (no spaces):
e.g.: ENSG00000189,ENSG123456790

* Output

Relative to the project directory, the following files will be generated:

- html/report.zip

Contains "report.html" and "data" folder.  The report can be opened offline by opening "report.html" in a web browser.

- igv/

Folder containing *.tdf files for each sample.  Can be used to view sequencing depth in IGV.

- cpg_density/

Folder containing .bed and .bed.idx files for each sample; needed to view CpG density in IGV.

- igv_snapshot/

Folder containing IGV-generated images of sequencing depth and CpG density for genes of interest.

- cpg_enrichment.txt

CpG enrichment in samples relative to unconverted reference genome.

Scripts
--------

* bisulfite_coverage_report.pl - Sets up environment, lanuches and coordinates between jobs.

* bisulfite_cpg_density.pl - Calculates CpG density for samples.

* bisulfite_cpg_enrichment.pl - Determines level of CpG enrichment in samples as compared to unconverted reference sequence.

* igv_png_bisulfite.pl - Prepare and transfer data for IGV.  Call "igv_bisulfite.py".

* igv_bisulfite.py - API to remotely interact with IGV, load appropriate tracks, and create .png snapshots.

* bisulfite_coverage_html.pl - Report results in HTML format.

