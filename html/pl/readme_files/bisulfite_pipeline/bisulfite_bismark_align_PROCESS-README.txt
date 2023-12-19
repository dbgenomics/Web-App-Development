Bisulfiteseq Bismark Align
Author: Nick Bild
Date: 2016-08-18
Version 1.0: Initial development.

Description
--------

Bisulfiteseq Bismark Align maps bisulfite treated sequencing reads to a genome of interest and produces methylation calls.

Script relationships:

bismark_align.pl

Dependencies
--------

Perl v5 is required.  Bismark is also required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

Bisulfiteseq Bismark Align is available via the bisulfiteseq pipeline (note that step numbers may change over time):

5. bismark align

* Values for the following entries in oap_database.txt will be asked for:

[BISMARK_BOWTIE2_GENOME]

To generate a bowtie2 index for Bismark, the following command can be used:

/opt/bismark_v0.15.0/bismark_genome_preparation --path_to_bowtie /opt/bowtie2-2.2.6/ /home/act/database/hsa/genome/hg38/bowtie2_index_bisulfite/

where "/home/act/database/hsa/genome/hg38/bowtie2_index_bisulfite/" is the path to a genome FASTA file and the directory in which the index will be written.

* Output

The following files will be generated:

<PROJ_DIR>/bismark/<SPLIT-SAMPLE-NAME>/<SPLIT-SAMPLE-NAME>.fastq_bismark_bt2.bam			-- contains all alignments plus methylation call strings
<PROJ_DIR>/bismark/<SPLIT-SAMPLE-NAME>/<SPLIT-SAMPLE-NAME>.fastq_bismark_bt2_splitting_report.txt	-- contains alignment and methylation summary
<PROJ_DIR>/bismark/<SPLIT-SAMPLE-NAME>/CpG_context_<SPLIT-SAMPLE-NAME>.fastq_bismark_bt2.txt		-- context dependent methylation
<PROJ_DIR>/bismark/<SPLIT-SAMPLE-NAME>/CHH_context_<SPLIT-SAMPLE-NAME>.fastq_bismark_bt2.txt		-- context dependent methylation
<PROJ_DIR>/bismark/<SPLIT-SAMPLE-NAME>/CHG_context_<SPLIT-SAMPLE-NAME>.fastq_bismark_bt2.txt		-- context dependent methylation

Scripts
--------

* bismark_align.pl - Performs Bismark alignments.

