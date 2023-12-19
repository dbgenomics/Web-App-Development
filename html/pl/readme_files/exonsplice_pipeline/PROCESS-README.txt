Exon Splice Pipeline
Author: Nick Bild
Date: 2016-09-21
Version 1.0: Initial development.

Description
--------

The Exon Splice Pipeline will detect and quantify splice junctions, and calculate differential exon usage.

Script relationships:

splice_counts.pl
|
-- splice_dexseq.pl
   |
   -- splice_dexseq_reorder.pl
      |
      splice_dexseq_anno.pl 

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.

Required R modules:
DEXSeq
parallel

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/ and /home/act/software/yonggan/.

Usage Instructions
--------

The Exon Splice Pipeline is available as the "exonsplice" pipeline.  The following steps are available (note that step numbers may change over time):

1. rename R0 files to R1
2. fastq split and qc
3. fastq filter and trim
4. estimate pair distance and tophat align
5. tophat alignment
6. raw counts
7. DEXSeq
8. annotate DEXSeq

The above steps are intended to be ran in the order that they appear.

- rename R0 files to R1, fastq split and qc, fastq filter and trim

These data preprocessing steps are borrowed from the tophatanalysis2 pipeline, and should be used in the same way with the splice pipeline.

- estimate pair distance and tophat align, or tophat alignment

This is a modified version of the tophatanalysis2 steps of the same name.  This version will accept an annotation GTF as input for use in splice junction detection, and otherwise operate in the same manner as the tophatanalysis2 versions.

Output:

<PROJ_DIR>/tophat/<SPLIT_SAMPLE>/junctions.bed			-- Detected splice junctions.

junctions.bed is of the format:
col 1 - chromosome
col 2 - start pos.
col 3 - stop pos.
col 4 - junction name
col 5 - number of reads containing this junction.
col 6 - strand 

- raw counts

This step produces the raw counts needed for input to DEXSeq.

You will be asked if the reads are paired, the HTSeq-count strandedness (yes/no/reverse) and for DEXSeq annotation.  Note that DEXSeq annotation is a flattened version of the Ensembl GTFs that must be prepared individually for each species/version by DEXSeq scripts.  Here is an example:

python /home/raid_opt/R/library/DEXSeq/python_scripts/dexseq_prepare_annotation.py ensembl_Mus_musculus.GRCm38.83.chr_edit.gtf ensembl_Mus_musculus.GRCm38.83.chr_edit.DEXSeq.gtf

In this case, "ensembl_Mus_musculus.GRCm38.83.chr_edit.gtf" will be converted to DEXSeq annotation named "ensembl_Mus_musculus.GRCm38.83.chr_edit.DEXSeq.gtf".

Output:

<PROJ_DIR>/splice_junction_counts/<SAMPLE>.txt			-- Sample level counts.

- DEXSeq

This step calculates differential exon usage.

You'll be asked to supply the sampleinfo file and DEXSeq annotation.

Output:

<PROJ_DIR>/splice_junction_differential/dexseq_results.reorder.sort.txt		-- Cleaned and reordered DEXSeq output.

And for each of the top 10 genes (by lowest p-value):
<PROJ_DIR>/splice_junction_differential/<GENEID>.png				-- Visualization of transcript models.

Alternate methods of selecting the top 10 genes are not presently available as DEXSeq only supports simple 2 level comparisons.

Sampleinfo:
The sampleinfo file is expected to have grouping information in column 6.  DEXSeq can only support 2 levels.

- annotate DEXSeq

This step will annotate the DEXSeq output.

You'll be asked for the correct biomart export to annotate the data with.

Output:
<PROJ_DIR>/splice_junction_differential/dexseq_results.reorder.sort.anno.txt         -- The final cleaned, reordered, and annotated DEXSeq output.

Column definitions:

Counting Bin ID				-- group/gene identifier
Ensembl Gene ID
Exon ID
Associated Gene Name
Description
Chromosome
Counting Bin Start (bp)			-- coordinates of the exon/feature
Counting Bin End (bp)			-- coordinates of the exon/feature
Counting Bin Width (bp)			-- range of start/end counting bin
Strand
Overlapping Transcript IDs		-- list of transcripts overlapping with the exon
Entrez Gene ID
Biotype
Differential Exon Usage P Value		-- LRT p-value: full vs reduced
Differential Exon Usage FDR		-- BH adjusted p-values
Estimated Exon Use Fold Change		-- relative exon usage fold change
SL...					-- raw counts for each sample

Scripts
--------

* splice_counts.pl - Prepare raw counts for DEXSeq.

* splice_dexseq_anno.pl - Annotate DEXSeq output.

* splice_dexseq.pl - Run DEXSeq.

* splice_dexseq_reorder.pl - Reorder and sort DEXSeq output.

* tophat_align_pair_dist_comb_splice.pl - Determine distance between read pairs, align and detect splice junctions.

* tophat_align_splice.pl - Align reads, detect splice junctions.

