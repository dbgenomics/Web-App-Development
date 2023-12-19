Noncoding-RNA Pipeline
Author: Nick Bild
Date: 2016-01-28
Version 1.0: Initial development.
Date: 2016-05-02 NAB
Updated this document to make usage of pipeline version of software more clear.
Date: 2016-06-17 NAB
Split filtering and annotation column re-ordering into a separate step.
Update log output.
Index BAM files.
Rename threshold.txt to ncrna_threshold.txt.
Make ncrna_final folder.
Date: 2016-06-20 NAB
Add RPMs, annotated and filtered.
Add RPM threshold file.
Rename ncrna_threshold.txt to RPM-threshold-ncRNA.txt.
Renamed total_count_bammerge.txt to total_count_bammerge_ncrna.txt.
Added summary tables.

Description
--------
The Noncoding-RNA Pipeline aligns FASTQ files to a genome with bowtie2, counts features with bedtools, and generates RPKM values.  Reports, and filtered reports, are generated from the results.  Counts are annotated via the RNA Central web API.

Script relationships:

34. ncRNA Align and Count Features

ncrna_step2.pl
|
-- process2.pl

35. ncRNA Report and Annotate

ncrna_step3.pl
|
-- process3.pl

36. ncRNA Filter and Re-order Annotation

ncrna_step4.pl
|
-- filter.pl
|
-- reorder_cols.pl
|
-- ncrna_reports.pl

Dependencies
--------

Perl v5 is required.  The perl scripts must all be located in the same directory for proper function.

Perl modules LWP::Simple and JSON::PP are also required and can be obtained via CPAN.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/ncrna_pipeline.

Usage Instructions
--------

* The pipline is available as part of the tophatanalysis2 pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

34. ncRNA Align and Count Features
35. ncRNA Report and Annotate
36. ncRNA Filter and Re-order Annotation

The steps are ran in the order that they appear, from the project directory.  The steps are compatible with the output of "1. fastq split and qc" and look for FASTQ files in the "fastq_tophat" folder.

34. ncRNA Align and Count Features -- this step will ask you to select an appropriate Bowtie index and GTF annotation.  The following output will be generated:

<PROJ_DIR>/bowtie/<SAMPLENAME-SPLIT>/<SAMPLENAME-SPLIT>.bam     -- Alignments
<PROJ_DIR>/counts/<SAMPLENAME-SPLIT>/counts.txt                 -- Counts

35. ncRNA Report and Annotate -- this step will ask you to select an appropriate GTF annotation file.  

This step will merge the split results into a final report.

36. ncRNA Filter and Re-order Annotation -- this step will ask you to select an appropriate GTF annotation file.

The user will also be asked:

- Specify the percentage of samples that must have >=50 counts to pass filter (e.g. 25, leave blank to specify 1+ samples):

After completion, the following output will be produced:

<PROJ_DIR>/final/<SAMPLENAME>/combined.annotated.txt		-- Annotated feature counts
<PROJ_DIR>/final/<SAMPLENAME>.bam				-- Merged BAM files
<PROJ_DIR>/final/stats.txt					-- Alignment stats
<PROJ_DIR>/final/combined.txt					-- Feature counts, all samples
<PROJ_DIR>/final/combined.annotated.txt				-- Annotated feature counts, all samples
<PROJ_DIR>/final/combined.annotated.txt.orig            	-- Annotated feature counts, all samples, annotation at end.
<PROJ_DIR>/final/RPKM-threshold-ncRNA.txt			-- RPKM Thresholds
<PROJ_DIR>/final/RPM-threshold-ncRNA.txt               		-- RPM Thresholds
<PROJ_DIR>/final/combined.annotated.filtered.txt		-- Filtered annotated feature counts
<PROJ_DIR>/final/combined.annotated.filtered.txt.orig   	-- Filtered annotated feature counts, annotation at end.
<PROJ_DIR>/final/combined.rpkm.txt				-- RPKMs, all samples
<PROJ_DIR>/final/combined.rpkm.filtered.txt			-- Filtered RPKMs, all samples
<PROJ_DIR>/final/combined.rpm.txt				-- RPMs, all samples.
<PROJ_DIR>/final/combined.rpm.filtered.txt			-- Filtred RPMs, all samples.
<PROJ_DIR>/final/combined.rpm.annotated.filtered.txt		-- Filtred RPMs, all samples, annotated.
<PROJ_DIR>/final/combined.annotated.summary.percentages.txt	-- rna_type summary, percentages.
<PROJ_DIR>/final/combined.annotated.summary.counts.txt		-- rna_type summary, raw counts.

These output files are at the sample level.  They are the final output.  Annotated files contain 19 annotation columns:

geneID	url	md5	length	xrefs	publications	database	id	description	external_id	optional_id	species	rna_type	gene	product	organelle	citations	source_url	expert_db_url

Note that this step will take several hours to complete due to the numerous web API requests to RNA Central for annotation lookups.  287,000 annotation lookups take approx. 7 hours to complete.  Note that this is variable due to network conditions and RNA Central capacity at any given time.

A typical run would follow this workflow:

1. fastq split and qc
2. fastq filter and trim    (OPTIONAL)
34. ncRNA Align and Count Features
35. ncRNA Report and Annotate
36. ncRNA Filter and Re-order Annotation

* Filtering

Filtered files by default include only genes in which 1+ samples contain >= 50 counts.  Alternatively, a user may specify the minimum percentage of samples that must have >= 50 counts.

Any samples with a count <10 will be replaced with the replacement value in the <PROJ_DIR>/final/threshold.txt file.

* RPKM Generation

RPKM values are generated with the formula:

rpkm = counts / ( (genelength / 1000) * (totalreads / 1000000) );

where totalreads is the number of unique aligned FASTQ tags.

genelength is calculated as the gene end position - gene start position + 1.

* Threshold file generation

The RPKM threshold values are calculated as follows:

RPKM1:  ((1 / (avggenelen / 1000)) / (totalreads / 1000000))
RPKM10: ((10 / (avggenelen / 1000)) / (totalreads / 1000000))
RPKM50: ((50 / (avggenelen / 1000)) / (totalreads / 1000000))

The RPM threshold values are calculated as follows:

RPM1:  1 / (totalreads / 1000000)
RPM10: 10 / (totalreads / 1000000)
RPM50: 50 / (totalreads / 1000000)


where totalreads is the number of unique aligned FASTQ tags, and avggenelen is the NCRNAAVGGENELEN value in ~/software/yonggan/oap_database.txt for the selected species.

The replacement value is the average RPKM10 value across all samples.

* Creating Indexes and Annotation:

- Filter the full RNA Central database into a species (or multiple) specific
  FASTA:

Modify the perl script to specify the correct species, then run it with the
full RNA Central database as the input.

/home/act/database/rnacentral_v3/rattus_norvegicus/bowtie2_index/parse.pl
/home/act/database/rnacentral_v3/bowtie2_index/rnacentral_active_v3.fa >
out.fa

- Trim poly-A/T tails:

/opt/bin/prinseq-lite-0.20.4/prinseq-lite.pl -fasta out.fa -out_good
out.trimmed.fa -trim_tail_left 5 -trim_tail_right 5

- Build the Bowtie index as usual (/opt/bin/bowtie2-build) from the trimmed
  FASTA file.

- To create the annotation, run:

/home/act/software/nickbild/ncrna_pipeline/create_annotation.pl out.trimmed.fa
> out.gff

Scripts
--------

* gen_cfg.pl - This generates config files automatically when the pipeline is ran via the tophatanalysis2 pipeline.  It converts the original config file based pipeline into a pipeline compatible with the desired tophatanalysis2-style format.

* ncrna_step2.pl - Calls process2.pl for all FASTQ files in the sampleinfo file.

* process2.pl - Aligns FASTQ files with bowtie2 and counts features with bedtools.

* ncrna_step3.pl - Calls process3.pl for all FASTQ files in the sampleinfo file.

* process3.pl - Merges BAM and count files, and generates combined reports with RNA Central annotation.

* ncrna_step4.pl -Calls filter.pl and reorder_cols.pl.

* filter.pl - Generates RPKM values, and filters both counts and RPKM values.  Inserts RPKM replacement values for low RPKM values.

* reorder_cols.pl - Re-order annotation such that it precedes data.

* create_annotation.pl - Convert RNA Central FASTA into GFF annotation.

* ncrna_reports.pl - Generates summary reports.
 
