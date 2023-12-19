Merge Multiple Data Tables
Author: Nick Bild
Date: 2016-05-03
Version 1.0: Initial development.

Description
--------

The Merge Multiple Data Tables pipeline will merge any number of text-delimited annotated data files.

Script relationships:

merge_datatables_generic.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the statanalysis pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

1. Merge multiple data tables

The following questions will be asked:

Enter a comma-delimited list of files to include.
 e.g.: /path/to/project1/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project2/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project3/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt
Enter the number of annotation columns in the data files:
 e.g.: 8
Which column contains the key to merge files on?
 e.g.: 1

The input files must be tab-delimited text files that all have the same structure, including one header row, the same number of annotation columns, data columns following annotation columns, and the same set of unique keys (1 per row).  If any key exists which is not included in all files, the pipeline will exit with an error message.

The merged output will be stored in the "merged_file" directory, under the current working directory.  The output file is named "merged_output.txt".

* To run the pipeline manually:

cd to the project directory, then run:

/home/act/software/nickbild/merge_datatables_generic.pl

The workflow matches the pipeline version after this point.

* The legacy easyRNASeq merging tool is available via the command line only.

cd to the project directory, then run:

/home/act/software/nickbild/merge_counts.pl

The following question will be asked:

Enter a comma-delimited list of files to include.
e.g.: /path/to/project1/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project2/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project3/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt
ONLY include the '_raw_genes' files!  RPKM and exon files will automatically be included.
Files:
 e.g.: /path/to/project1/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project2/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt,/path/to/project3/easyrnaseq/easyRNASeq_Anno_Bista_genes_raw.txt

The merged output will be stored in the "merged_counts" directory, under the current working directory.

Scripts
--------

* merge_datatables_generic.pl - Merge multiple data tables.

* merge_counts.pl - Merge multiple easyRNASeq result files.  Legacy code.

