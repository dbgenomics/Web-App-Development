Trinity Metagenome Pipeline
Author: Nick Bild
Date: 2016-08-02

Description
--------

The Trinity Metagenome Pipeline assembles a transcriptome with Trinity, filters the transcriptome with RSEM, and generates annotation for the transcripts with Trinotate.  All reads are then aligned to the transcriptome with bowtie2, counts are generated with HTSeq-count, and merged count and RPM files are produced.  The merged files can be filtered by user-specified criteria.

Script relationships:

2. prepare reads and run Trinity

trinity_run.pl

3. filter transcripts with RSEM

trinity_rsem_run.pl
|
-- filter_rsem.pl

4. generate annotation database

trinity_annotate_gen.pl
|
-- trinity_gtf.pl

5. bowtie2 align

trinity_bowtie2.pl

6. merge bowtie bam

trinity_merge_bam.pl

7. sort BAM, BAM to SAM

SortBAM2SAM.pl

8. htseq-count

HTSeq_Count-trinity.pl

9. generate RPMs

trinity_gen_rpm.pl

10. merge count/RPM files

MergeCountFiles-trinity.pl

11. annotate counts/RPMs

trinity_anno_counts.pl

12. filter counts/RPMs

filter_trinity.pl

Dependencies
--------

Perl v5 is required.

Perl modules LWP::Simple and JSON::PP are also required and can be obtained via CPAN.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/ and /home/act/software/yonggan/.

Usage Instructions
--------

* The pipline is available as part of the metatrinity pipeline (note that step numbers may change over time):

1. fastq split and qc
2. prepare reads and run Trinity
3. filter transcripts with RSEM
4. generate annotation database
5. bowtie2 align
6. merge bowtie bam
7. sort BAM, BAM to SAM
8. htseq-count
9. generate RPMs/RPKMs
10. merge count/RPM/RPKM files
11. annotate counts/RPMs/RPKMs
12. filter counts/RPMs/RPKMs

The steps are ran in the order that they appear.

1. fastq split and qc

Splits FASTQ files and generates QC report.

Output:

fastq_tophat/				-- FASTQ files.
QC-results/				-- FastQC results.

2. prepare reads and run Trinity

Samples reads from all samples, and runs them as input for Trinity.

The following questions will be asked:

- Node	Memory (GB)	# Reads Recommended	% Reads Per Sample
- node01	62.8G	62 million	22
- node02	62.8G	62 million	22
- node03	315.3G	315 million	100
- node04	62.8G	62 million	22
- node05	62.9G	62 million	22
- node06	62.9G	62 million	22
- node07	62.9G	62 million	22
- Choose a host to run the job on (enter value from 'Node' column):
e.g.: node03

- Enter the total number of reads to include across all samples in millions (e.g. enter '60 for '60000000'):
e.g.: 80

A column with the header "Pct Representation" may be included in the sampleinfo file.  If present, it will determine the percentage of reads from each sample that will be represented in the Trinity input.  Use whole numbers, e.g. "25" to indicate 25%.  Column total should be 100.  If this column is not present, all samples will be equally represented in the trinity input.

Example sampleinfo:

----
#Sequencing Data ID	Sample Name	ORB Enriched DNA Library ID	Customer ID	Project	Factor 1	Factor 2	Factor 3	PCT Representation
SL139437	3635-CN-0001	CM4803801	B87644-1	Gregorio	NA	NA	NA	10
SL139438	3635-CN-0002	CM4803802	B87644-2	Gregorio	NA	NA	NA	10
SL139439	3635-CN-0003	CM4803803	B84996-1	Gregorio	NA	NA	NA	10
SL139440	3635-CN-0004	CM4803804	B84996-2	Gregorio	NA	NA	NA	10
SL139441	3635-CN-0005	CM4803805	B14488-1	Gregorio	NA	NA	NA	10
SL139442	3635-CN-0006	CM4803806	B14488-2	Gregorio	NA	NA	NA	50
----

- Enter the strand-specific RNA-Seq read orientation (if paired: 'RF' or 'FR', if single: 'F' or 'R'):
e.g. FR

Help for this option can be found at:
https://github.com/trinityrnaseq/trinityrnaseq/wiki/Running%20Trinity

Output:

trinity_input/r1.fastq			-- R1 for input to Trinity.
trinity_input/r2.fastq			-- R2 for input to Trinity.
trinity/Trinity.fasta			-- Assembled transcriptome.

3. filter transcripts with RSEM

Runs RSEM and filters transcriptome based on results.  Each transcript must compose >5% of all transcripts for a given gene to be kept.

- Enter the strand-specific RNA-Seq read orientation (if paired: 'RF' or 'FR', if single: 'F' or 'R'):
e.g. FR

Help for this option can be found at:
https://github.com/trinityrnaseq/trinityrnaseq/wiki/Running%20Trinity

Output:

trinity/trinity_rsem_filtered.fasta	-- RSEM filtered transcriptome.
rsem/<SAMPLENAME>.isoforms.results	-- Raw RSEM results.

4. generate annotation database

Generates an annotation database with Uniprot and Pfam-A data using Trinotate.

The following questions will be asked:

- For transdecoder, should the reads be considered strand-specific (only analyzes top strand -- enter 'y' or 'n')?
e.g.: Y

For help on this option, see:
https://transdecoder.github.io/

Output:

trinotate/blastx.outfmt6				-- Uniprot blastx results.
trinotate/blastp.outfmt6				-- Uniprot blastp results.
trinotate/TrinotatePFAM.out				-- Pfam-A hmmscan results.
trinotate/trinotate_annotation_report.txt		-- Final annotation file.
trinotate/trinotate_annotation_report_transform.txt	-- Final annotation file, transformed.
gtf/genome.gtf						-- GTF for feature counting.
trinity/trinity_rsem_filtered.annotated.fasta		-- Annotated, filtered FASTA file.

5. bowtie2 align

Aligns reads to transcriptome.

Output:

bowtie/<SAMPLENAME>/<SAMPLENAME>.bam		-- Split sample level BAM file.

6. merge bowtie bam

Merges split BAM files into sample level BAM files.

Output:

bam/<SAMPLENAME>.bam				-- Sample level BAM file.
total_count_bammerge.txt			-- Total counts for all samples.

7. sort BAM, BAM to SAM

Sorts BAM files by tag name, and converts them to SAM (in preparation for HTSeq-count).

Output:

bam/<SAMPLENAME>_sorted.bam			-- Tag name sorted BAM file.
bam/<SAMPLENAME>.sam				-- Tag name sorted SAM file.

8. htseq-count

Counts features for each sample.

The following questions will be asked:

- Skip all reads with alignment quality lower than this value (e.g. 10):
e.g.: 0

- Values for the following attributes in oap_database.txt will be asked for:

HTSEQSTRAND
HTSEQINTERSEC

The impact of these options can be found here:
http://www-huber.embl.de/users/anders/HTSeq/doc/count.html

Output:

htseq/gene_<SAMPLENAME>.txt			-- Feature counts.

9. generate RPMs/RPKMs

Generate RPM/RPKM values.

Output:

htseq/rpm_<SAMPLENAME>.txt			-- RPM values for sample.
htseq/rpkm_<SAMPLENAME>.txt                      -- RPKM values for sample.

10. merge count/RPM/RPKM files

htseq/HTSeq_Count_hsa_genes.txt			-- Raw counts, merged.
htseq/HTSeq_Count_hsa_rpm.txt			-- RPMs, merged.
htseq/HTSeq_Count_hsa_rpkm.txt                   -- RPKMs, merged.

11. annotate counts/RPMs/RPKMs

Annotate merged raw counts, RPKMs, and RPMs.

Output:

htseq/HTSeq_Anno_hsa_genes.txt			-- Raw counts, merged, annotated.
htseq/HTSeq_Anno_hsa_rpm.txt			-- RPMs, merged, annotated.
htseq/HTSeq_Anno_hsa_rpkm.txt                    -- RPKMs, merged, annotated.

12. filter counts/RPMs/RPKMs

Filter raw counts RPKMs, and RPM values.

The following question will be asked:

- Specify the percentage of samples that must have >=50 counts to pass filter (e.g. 25, leave blank to specify 1+ samples):
e.g.: 50

Output:

meta-trinity-rpm-thresholds.txt			-- RPM thresholds.
meta-trinity-rpkm-thresholds.txt                -- RPKM thresholds.
meta-trinity_total_count_bammerge.txt		-- Total counts.
htseq/HTSeq_Anno_hsa_genes.filtered.txt		-- Filtered raw counts.
htseq/HTSeq_Anno_hsa_rpm.filtered.txt		-- Filtered RPMs.
htseq/HTSeq_Anno_hsa_rpkm.filtered.txt          -- Filtered RPKMs.

Scripts
--------

* filter_rsem.pl - Filter transcriptome by RSEM results.

* filter_trinity.pl - Filter raw counts and RPM values.

* HTSeq_Count-trinity.pl - Count features with HTSeq-count.

* MergeCountFiles-trinity.pl - Merge raw count and RPM files.

* trinity_anno_counts.pl - Annotate count and RPM files.

* trinity_annotate_gen.pl - Generate an annotation database.

* trinity_bowtie2.pl - Align reads to transcriptome.

* trinity_gen_rpm.pl - Generate RPM files.

* trinity_gtf.pl - Create a GTF for feature counts.

* trinity_merge_bam.pl - Merge split BAM files.

* trinity_rsem_run.pl - Run RSEM.

* trinity_run.pl - Prepare FASTQ files and run Trinity.

