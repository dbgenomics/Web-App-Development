Metagenome Pipeline
Author: Nick Bild
Date: 2016-01-29
Version 1.0: Initial development.
Date: 2016-06-27 NAB
Add RPM values.
Add RPKM and RPM threshold files.
Break DESeq into a separate step.
Add filtering step.
Add Krona step to view Kraken output.
Added additional logging of user input and output file information.
Date: 2016-07-19 NAB
Add alignment report.

Description
--------
The Metagenome Pipeline splits FASTQ files, aligns them to a metagenome with bowtie2, gets feature counts with HTSeq-count, performs differential expression with DESeq, and generates RPKM/RPM values.  Filtering can be performed on count/RPM/RPKM values.

The separate Kraken pipeline classifies sequences from the raw FASTQ files, and reports are generated from the Kraken output.  Kraken results can be visualized in HTML report via Krona.

Script relationships:

2. Align and Count

metagenome_step2.pl
|
-- process2.pl

3. Merge BAM and Counts

metagenome_step3.pl
|
-- process3.pl
   |
   -- qsub_generic.pl (merge BAM)

4. RPKM and RPM

metagenome_step4.pl

5. Merged Reporting

metagenome_step5.pl
|
-- process5.pl
   |
   -- filter.pl

6. Filtering

filter_custom.pl

7. DESeq2

deseq_step.pl
|
-- deseq2.pl
   |
   -- merge_tables.pl

8. Kraken Classification

kraken_step1.pl
|
-- mpa-report-combined.pl
|
-- class-parse.pl
|
-- kraken_reports.pl

9. Krona Visualization

krona_step1.pl
|
-- run_krona.pl

Dependencies
--------

Perl v5 is required.  The perl scripts must all be located in the same directory for proper function.

Perl modules LWP::Simple and JSON::PP are also required and can be obtained via CPAN.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/metagenome.

Usage Instructions
--------

* The pipline is available as part of the meta pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

1. fastq split and qc
2. Align and Count
3. Merge BAM and Counts
4. RPKM and RPM
5. Merged Reporting
6. Filtering
7. DESeq2
8. Kraken Classification
9. Krona Visualization

The steps are ran in the order that they appear, with step 6 onward being optional.

2. Align and Count

- Align sequences with bowtie2 (split).
- Get feature counts with HTSeq-count (split).

Output:

<PROJ_DIR>/bowtie/<SAMPLENAME-SPLIT>/<SAMPLENAME-SPLIT>.bam	-- Alignments
<PROJ_DIR>/counts/<SAMPLENAME-SPLIT>/counts.txt			-- Counts

3. Merge BAM and Counts

Output:

<PROJ_DIR>/final/<SAMPLENAME>/counts.txt			-- Feature counts
<PROJ_DIR>/final/combined.txt					-- Feature counts, samples combined
<PROJ_DIR>/final/<SAMPLENAME>.bam				-- Merged BAM files
<PROJ_DIR>/final/<SAMPLENAME>.<FEATURENAME>.spot-check.sam	-- Spot check SAM files
	
4. RPKM and RPM

- Get RPKM/RPM values.
- Alignment statistics.

Output:

<PROJ_DIR>/final/meta-rpkm-thresholds.txt				-- RPKM thresholds file
<PROJ_DIR>/final/meta-rpm-thresholds.txt				-- RPM thresholds file
<PROJ_DIR>/bowtie/<SAMPLENAME-SPLIT>/<SAMPLENAME-SPLIT>.bam.summary	-- Alignments stats
total_count_bammerge.txt						-- Total aligned read counts
<PROJ_DIR>/final/<SAMPLENAME>.rpkm.txt					-- Sample level RPKM data
<PROJ_DIR>/final/<SAMPLENAME>.rpm.txt					-- Sample level RPM data
<PROJ_DIR>/final/bowtie_report.txt					-- Alignment report.

5. Merged Reporting

- Merge sample level data into combined reports.

Output:

<PROJ_DIR>/final/rpm.merged.annotated.txt				-- Merged RPM values, annotated
<PROJ_DIR>/final/rpm.merged.txt						-- Merged RPM values
<PROJ_DIR>/final/rpkm.merged.annotated.txt				-- Merged RPKM values, annotated
<PROJ_DIR>/final/rpkm.merged.txt					-- Merged RPKM values
<PROJ_DIR>/final/combined.annotated.txt					-- Merged raw counts

6. Filtering

- Filter raw counts and RPKM/RPM data.

Output:

<PROJ_DIR>/final/final/combined.annotated.filtered.txt			-- Combined counts, filtered
<PROJ_DIR>/final/final/rpkm.merged.annotated.filtered.txt		-- Combined RPKM, filtered
<PROJ_DIR>/final/final/rpm.merged.annotated.filtered.txt		-- Combined RPM, filtered

7. DESeq2

You will need to generate a config file to specify the comparisons you'd like to make.

The format looks like:

deseq_1_name=SL139441-SL139442_x_SL139443-SL139444
deseq_1_r1=SL139441merged&SL139443merged
deseq_1_r2=SL139442merged&SL139444merged
deseq_2_name=SL139441_x_SL139442
deseq_2_r1=SL139441merged&SL139442merged

In this example, there are 2 comparisons (keys start with "deseq_1_" and
"deseq_2_" for comparison 1 and 2, respectively.  Each comparison will have a
name key, e.g. "deseq_1_name" that specifies a name for the comparison being
made (examples above are good practice).  They will also have one or more "r"
(replicate) keys specifying the samples to be compared.  The samples on the
left side of the "&" delimter are on the "left" side of the comparison, and
the samples on the right are on the "right" side of the comparison.  So, in
example 1 above, the "left" side of the comparison contains the replicates
SL139441merged and SL139442merged (one condition) compared to the replicates
SL139443merged and SL139444merged (the second condition).  Sample names are
the FASTQ names, with "_R1_" and ".fastq" removed (NOTE: in the updated marburg
pipeline, they are the sample names from the sampleinfo file).

Output:

final/deseq2/<COMPARISON>/out/DESeq_genes.csv				-- DESeq2 output

8. Kraken Classification

- Classify raw reads taxonomically.

Output:

<PROJ_DIR>/kraken/<SAMPLENAME>.kraken				-- Raw Kraken classification output
<PROJ_DIR>/kraken/<SAMPLENAME>.kraken.labels.mpa-format		-- Full taxonomic name added to raw output
<PROJ_DIR>/<SAMPLENAME>.kraken.report				-- Kraken result statistics
<PROJ_DIR>/kraken/all-samples.kraken.mpa-report			-- Kraken mpa-format report
<PROJ_DIR>/kraken/all-samples.kraken.mpa-report.formatted       -- Kraken mpa-format report, reformatted
<PROJ_DIR>/kraken/classification-species.counts			-- Taxon level report
<PROJ_DIR>/kraken/classification-genus.counts			-- Taxon level report
<PROJ_DIR>/kraken/classification-family.counts			-- Taxon level report
<PROJ_DIR>/kraken/classification-order.counts			-- Taxon level report
<PROJ_DIR>/kraken/classification-class.counts			-- Taxon level report
<PROJ_DIR>/kraken/classification-phylum.counts			-- Taxon level report
<PROJ_DIR>/kraken/kraken_<TAXON-LEVEL>_counts.txt		-- For each taxon and each sample, a count of the number of reads classified to that taxon in the given sample.
<PROJ_DIR>/kraken/kraken_<TAXON-LEVEL>_percentage.txt		-- For each taxon and each sample, the percentage of reads classified to the taxon within the given sample.
<PROJ_DIR>/kraken/kraken_<TAXON-LEVEL>_percentage.txt.png	-- Distribution of taxon counts for each sample as a stacked bar chart.

9. Krona Visualization

- Generate HTML reports of Kraken data.

Output:

<PROJ_DIR>/krona/all-samples.kraken.mpa-report.formatted.krona.<GROUPNAME-or-SAMPLE>.krona-input.txt
<PROJ_DIR>/krona/all-samples.kraken.mpa-report.formatted.krona.<GROUPNAME-or-SAMPLE>.krona-output.html
<PROJ_DIR>/krona/all-groups-samples.krona-output.html
<PROJ_DIR>/krona/all-groups.krona-output.html
<PROJ_DIR>/krona/all-samples.krona-output.html

Scripts
--------

* gen_cfg.pl - This generates config files automatically when the pipeline is ran via the meta pipeline.  It converts the original config file based pipeline into a pipeline compatible with the desired tophatanalysis2-style format.

* metagenome_step0.pl - Calls gunzip.pl for all FASTQ files in the sampleinfo file.

* gunzip.pl - gunzips compressed FASTQ files.

* metagenome_step1.pl - Calls process1.pl for all FASTQ files in the sampleinfo file.

* process1.pl - Calls split_fastq.pl for a FASTQ file.

* split_fastq.pl - Splits FASTQ files by the specified number of lines.

* metagenome_step2.pl - Calls process2.pl for all FASTQ files in the sampleinfo file.

* process2.pl - Aligns FASTQ files with bowtie2 and counts features with HTSeq-count.

* metagenome_step3.pl - Calls process3.pl for all FASTQ files in the sampleinfo file.

* process3.pl - Merges BAM and count files, and generates spot check data.

* metagenome_step4.pl - Gets unique tag counts and generates thresholds file.  Generates RPKM values.  Calls rpkm2.pl and deseq2.pl.

* rpkm2.pl - Calculates RPKM values.

* run_deseq_step.pl - Prepare DESeq input and call deseq2.pl.

* deseq2.pl - Performs differential expression comparisons with DESeq2.  Calls merge_tables.pl.

* merge_tables.pl - Combined counts for DESeq2.

* metagenome_step5.pl - Calls process5.pl for all FASTQ files in the sampleinfo file.

* process5.pl - Annotate combined counts, combine and annotate RPKMs.  Call filter.pl

* filter.pl - Filter combined counts and RPKMs.  Replaced by filter_custom.pl

* kraken_step1.pl - Run Kraken on FASTQ files.  Calls mpa-report-combined.pl and class-parse.pl.

* mpa-report-combined.pl - Reformat the Kraken mpa reports.

* class-parse.pl - Generate classification counts for each taxon level.

* krona_step1.pl - Gather files and group information for Krona.

* run_krona.pl - Prepare input files and generate HTML reports for each group from Kraken data.

* filter_custom.pl - Filter counts, RPMs, and RPKMs according to user input.

* kraken_reports.pl - Generates taxon-level counts/percentages as tables and plots.

