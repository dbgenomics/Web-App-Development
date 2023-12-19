Dr. Doyle's Renormalization
Author: Nick Bild
Date: 2016-05-23
Documentation of code previously developed primarily by Yonggan and Kevin.

Description
--------

Dr. Doyle's Renormalization calculates RPKM values for raw counts.  The total count used in the RPKM calculation is derived from nuclear protein coding genes only.

Script relationships:

easyrnaseq_norm.pl
|
-- Doyle_renorm_2016-01-23.R

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.

R libraries required:
dplyr
reshape2
magrittr

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/Doyle_renorm_2016-01-23.R and /home/act/software/yonggan/easyrnaseq_norm.pl.

Usage Instructions
--------

Dr. Doyle's Renormalization is available as part of the tophatanalysis2 pipeline (note that step numbers may change over time):

21. Dr. Doyle's renormalization

Input for the script is (oap_database.txt identifiers):

[ANNO_NOMIT_GENE] - a subset of the [ANNO_BIOMART_GENE] file, containing only protein coding genes.
[GENELEN] - gene lengths.

Gene and exon counts are automatically selected from <PROJECT_DIR>/easyrnaseq/easyRNASeq_Anno_*_genes_raw.txt and <PROJECT_DIR>/easyrnaseq/easyRNASeq_Anno_*_exons_raw.txt, respectively.

An "Ensembl Gene ID" column is required in [ANNO_NOMIT_GENE] as well as the raw count files.

Output:

<PROJECT>-nuclear-mRNA-total-count.txt	- Total counts for genes contained in [ANNO_NOMIT_GENE]
*gene_raw_nomit.txt    			- Raw gene counts for nuclear genes
*gene_rpkm.txt         			- Re-normalized RPKM values for all genes
*gene_rpkm_nomit.txt   			- Re-normalized RPKM values for nuclear genes
*exon_raw_nomit.txt    			- Raw exon counts for nuclear genes
*exon_rpkm.txt         			- Re-normalized RPKM values for all exons
*exon_rpkm_nomit.txt   			- Re-normalized RPKM values for nuclear exons

Scripts
--------

* easyrnaseq_norm.pl - Collect user input and call Doyle_renorm_2016-01-23.R.

* Doyle_renorm_2016-01-23.R - Perform RPKM calculations.

