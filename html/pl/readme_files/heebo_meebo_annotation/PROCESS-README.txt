HEEBO-MEEBO Annotation Generation Workflow
Author: Nick Bild
Date: 2016-05-18
Version 1.0: Initial development.

Description
--------

The HEEBO-MEEBO Annotation Generation Workflow generates the annotation files needed for the HEEBO MEEBO web app at: http://192.168.0.16/pl/gene_meebo_heebo_2016/form.html.

Script relationships:

extract_seq_list.pl

parse_sam.pl
|
-- parse_sam_summary.pl

get_coords.pl
|
-- get_features.pl
   |
   -- parse_features.pl
     |
     -- filter_features.pl
     |
     -- filter_features2.pl

extract_exons.pl
|
-- filter_features3.pl

gen_anno_report.pl
|
-- filter_features4.pl
   |
   -- gen_anno_report_combined.pl

find_dupes.pl

remove_dupes.pl

merge_anno.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/heebo-meebo.

Usage Instructions
--------

cd to /home/act/software/nickbild/heebo-meebo

"mmu_annotations_2011.txt" is an older set of annotations to update.

# Get sequence list.
./extract_seq_list.pl mmu_annotations_2011.txt 2016-04-05-MEEBO-Lot-50336-Mouse-Oligos mmu

# Align sequences, no seed mismatches.
bowtie2 -N 0 -p 2 -x bowtie2_index/Mus_musculus.GRCm38.cdna.all -f -U 2016-04-05-MEEBO-Lot-50336-Mouse-Oligos.fa -S align.sam

# Only keep probes that aligned to same strand as target transcript.
samtools view -bS align.sam > align.bam
samtools view -f 16 align.bam > align.reverse-strand.sam
samtools view -h -F 16 align.bam > align.same-strand.sam

# Split reads by number of mismatches.
perl -ne "print if((/XM:i:0/) || (/^@/));" align.same-strand.sam > mismatch_0.sam
perl -ne "print if((/XM:i:[1-5]/) || (/^@/));" align.same-strand.sam > mismatch_5.sam
samtools view -bS align.same-strand.sam > align.same-strand.bam
samtools view -h -f 0x4 align.same-strand.bam > unaligned.initial.sam
perl -ne "print if((/XM:i:[6-9]/) || (/^@/));" align.same-strand.sam > mismatch_gt5.sam
cat mismatch_gt5.sam unaligned.initial.sam > unaligned.final.sam

# Generate a table summarizing SAM files.
./parse_sam.pl mismatch_0.sam 70 > sam_table.txt
./parse_sam.pl mismatch_5.sam 70 >> sam_table.txt
./parse_sam.pl unaligned.final.sam 70 >> sam_table.txt

# Summary of SAM table.
./parse_sam_summary.pl mismatch_0.sam mismatch_5.sam unaligned.final.sam align.reverse-strand.sam > sam_table.summary.txt

# Get genomic coordinates.
export PERL5LIB=/usr/local/lib/perl5/5.22.1:$PERL5LIB
./get_coords.pl sam_table.txt > sam_table.genomic-coords.txt

# Get genomic features.
./get_features.pl sam_table.genomic-coords.txt mus_musculus > sam_table.genomic-features.txt

# Parse feature JSON, then filter features.
./parse_features.pl sam_table.genomic-features.txt > sam_table.genomic-features.parse.txt
./filter_features.pl sam_table.genomic-coords.txt sam_table.genomic-features.parse.txt > sam_table.genomic-features.parse.filter.txt
./filter_features2.pl sam_table.genomic-features.parse.filter.txt > sam_table.genomic-features.parse.filter2.txt

# Add in exons.
./extract_exons.pl Mus_musculus.GRCm38.84.chr.gtf > Mus_musculus.GRCm38.84.exons.txt
./filter_features3.pl Mus_musculus.GRCm38.84.exons.txt sam_table.genomic-coords.txt sam_table.genomic-features.parse.filter2.txt > sam_table.genomic-features.parse.filter3.txt

# Create Anno report and prefer exon containing oligos over no exons.
./gen_anno_report.pl sam_table.txt sam_table.genomic-features.parse.filter3.txt > sam_table.genomic-features.parse.filter4.txt
./filter_features4.pl sam_table.genomic-features.parse.filter4.txt > sam_table.genomic-features.parse.filter5.txt
./gen_anno_report_combined.pl sam_table.txt sam_table.genomic-features.parse.filter5.txt > 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.txt

# Manually handle remaining duplicates.
./find_dupes.pl 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.txt > 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.dupes-only.txt

# *** Waiting for DW to remove dupes manually.
# DW says dupes are OK -- just pick first from a set of dupes after sorting by associated gene name.
sort -k1,1 -k14,14 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.dupes-only.txt > 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.dupes-only.txt.sort
./remove_dupes.pl 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.dupes-only.txt.sort 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.txt > 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.txt.dedupe

##
# Insert annotation back into input table.
##
./merge_anno.pl mmu_annotations_2011.txt 2016-04-05-MEEBO-Mouse-Probes-Ensembl-84-Anno.txt.dedupe > 2016-04-05-MEEBO-Mouse-Array-Ensembl-84-Anno.txt

Scripts
--------

* extract_seq_list.pl - Get FASTA sequence list from previous annotation.

* parse_sam.pl - Generate a table summarizing SAM files.

* parse_sam_summary.pl - Summary of SAM tables.

* get_coords.pl - Get coordinates of alignments from Ensembl REST API.

* get_features.pl - Get features associated with coordinates from Ensembl REST API.

* parse_features.pl - Parse the JSON features returned by Ensembl.

* filter_features.pl - Only keep features on same strand as oligo, and only keep gene features.

* filter_features2.pl - Decide which feature to keep if multiple exist.

* extract_exons.pl - Get exon info from Ensembl GTF.

* filter_features3.pl - Find exons that overlap oligo.

* gen_anno_report.pl - Create a formatted report.

* filter_features4.pl - Determine which exons to keep.

* gen_anno_report_combined.pl - Create a formatted report.

* find_dupes.pl - Find any remaining duplicate oligos.

* remove_dupes.pl - Only keep first oligo for each set of duplicates.

* merge_anno.pl - Insert annotation and format the final report.

