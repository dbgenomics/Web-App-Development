MirBase21 Probe Annotation and Design
Author: Nick Bild
Date: 2016-02-23
Version 1.0: Initial development.

Description
--------

The MirBase21 Probe Annotation and Design tools generate annotation by comparing mirBase21 data to existing mirBase19 annotation.  Probes are then designed for the newly annotated micro-RNAs.

Script relationships:

desired_tm_stats.pl
|
-- tm.py

filter.pl
|
-- compare.pl
   |
   -- design_probes.pl
      |
      -- tm.py
      |
      -- gen_blast_fa.pl
         |
         -- parse_blast.pl
            |
            -- merge_tables.pl

Dependencies
--------

Perl v5 is required.

blastn from ncbi-blast-2.3.0+ is required.

Python v2.7+ is required.  Bio.SeqUtils module must be installed.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/mirbase21_probe_annot.

Usage Instructions
--------

- To get desired melting temperature:

./desired_tm_stats.pl seqs.txt

Supply a list of sequences, and statistics will be provided to determine optimal and acceptable tms.

STEP 1: Create Annotation.

* To filter the mirBase FASTA into the species of interest:

./filter.pl mature.fa > mature.fa.filtered

* To generate new annotation tables:

./compare.pl 2016-02-23-Current-Probe-Designs.txt mature.fa.filtered

This will create the output files:

- Table-I-M21-New-Designs.txt - mirBase21 micro-RNAs that did NOT exist in the previous version.
- Table-II-M21-with-Existing-Designs.txt - mirBase21 micro-RNAs that did exist in the previous version.

STEP 2: Create Probe Designs.

* Initial probe designs:

./design_probes.pl ../Table-I-M21-New-Designs.txt > 1_initial_probes.txt

* Get input suitable for BLAST from initial designs:

./gen_blast_fa.pl 1_initial_probes.txt > 1_initial_probes.blast.fa

* BLAST the data:

/opt/ncbi-blast-2.3.0+/bin/blastn -task "blastn-short" -db blastdb/all_db -query 1_initial_probes.blast.fa -out 1_initial_probes.blast.out -outfmt "6 qacc sacc mismatch evalue length pident qseq sstrand"

The BLAST database used for mirBase21 is at:

/home/act/software/documentation/mirbase21_probe_annotation_and_design/blastdb/

* Parse the BLAST data:

./parse_blast.pl 1_initial_probes.txt 1_initial_probes.blast.out mature.fa.filtered > 1_initial_probes.blast-parse.txt

* Create a table with the final probe designs:

./merge_tables.pl ../Table-I-M21-New-Designs.txt 1_initial_probes.blast-parse.txt > final.txt

Scripts
--------

* filter.pl - Filter mirBase FASTA file down to the species of interest.

* compare.pl - Compare mirBase21 to existing mirBase19 probes and generate annotation.

* design_probes.pl - Generate the initial probes.  Reverse complement, check melting temperature, trim if necessary, and repeat hybrid region multiple times depending on hybrid region length.

* gen_blast_fa.pl - Create input suitable for BLAST from the initial probe data.

* parse_blast.pl - Parse the BLAST data.

* merge_tables.pl - Generate the final probe design report.

* tm.py - Calculate melting temperature for a given sequence.

* desired_tm_stats.pl - Supply a list of sequences, and statistics will be provided to determine optimal tm and acceptable tm range.

