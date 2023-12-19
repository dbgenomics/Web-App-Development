16s rRNA Pipeline
Author: Nick Bild
Date: 2016-09-26
Version 1.0: Initial development.

Description
--------

The 16s rRNA Pipeline will perform Qiime-based analyses of 16s rRNA sequencing data.

Script relationships:

16srrna_filter.pl
|
-- 16srrna_cluster.pl
   |
   -- annotate_out.pl
      |
      -- 16srrna_align.pl
         |
         -- 16srrna_krona.pl
            |
            -- 16srrna_otu_network.pl
               |
               -- 16srrna_summary.pl

Dependencies
--------

Perl v5 is required.  Python version 2.7 is required, with Qiime installed.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/.

Usage Instructions
--------

The 16s rRNA Pipeline is available as the "16srrna" pipeline.  The following steps are available (note that step numbers may change over time):

1. filter reads
2. cluster OTUs and pick representative sequence
3. generate annotated OTU count table
4. align representative OTU seqs and build tree
5. krona
6. create OTU network
7. summarize and visualize sample taxonomic composition

The above steps are intended to be ran in the order that they appear.

- filter reads

This step will filter FASTQ files.

Input FASTQ files are expected to be in:

<PROJ_DIR>/fastq/

and named:

<SAMPLENAME>.fastq

<SAMPLENAME> must match the sample names found in the sampleinfo file.

Output:

<PROJ_DIR>/16srrna_filter/all_samples.fna					-- Merged FASTA file, all samples.
<PROJ_DIR>/16srrna_filter/<SAMPLENAME>/seqs.fna					-- Filtered sequences.
<PROJ_DIR>/16srrna_filter/<SAMPLENAME>/split_library_log.txt			-- Log of filtering results.

- cluster OTUs and pick representative sequence

This step will pick OTUs based on sequence similarity within the reads, and pick a representative sequence for each OTU.

The required degree of similarity between sequences is determined by SEQ_SIMILARITY in oap_database.txt

Output:

<PROJ_DIR>/otu/otu_clusters.txt							-- Clustered OTU output.
<PROJ_DIR>/otu/otu_rep_set_taxon_map.txt					-- The OTU taxonomic assignment file.

- generate annotated OTU count table

This step merges individual OTU count tables in to a single annotated OTU count table for all samples.

Output:

<PROJ_DIR>/otu/uclust_anno_otu.txt                                              -- Annotated OTU count table.

- align representative OTU seqs and build tree

This step will align sequences with PyNAST and build a phylogenetic tree.

Output:

<PROJ_DIR>/align/all_samples_rep_set_aligned.fasta				-- PyNAST alignments.
<PROJ_DIR>/otu/otu_rep_set.tre          		                        -- Phylogenetic tree.
<PROJ_DIR>/otu/otu_rep_set.tre.png						-- PNG of phylogenetic tree (via Dendroscope).

- krona

This step will create a Krona visualization of the annotated OTU counts.

Output:

<PROJ_DIR>/krona/krona.html							-- Krona visualization

- create OTU network

This step will create an OTU network, which can be visualized in Cytoscape (http://www.cytoscape.org/).

Output:

<PROJ_DIR>/otu_network/otu_network/						-- OTU network files.
<PROJ_DIR>/otu_network/otu_network/otu_network.png				-- OTU network PNG (via Cytoscape)

- summarize and visualize sample taxonomic composition

This step will produce summary data tables and charts.

Output:

<PROJ_DIR>/otu_summary/otu_phylum_heatmap.pdf					-- Phylum level heatmap.
<PROJ_DIR>/otu_summary/otu_network/						-- OTU network files.
<PROJ_DIR>/otu_summary/taxa_summary/						-- Tables and charts of taxa composition.

Scripts
--------

* 16srrna_align.pl - Align sequences with PyNAST and generate phylogenetic tree.

* 16srrna_cluster.pl - Cluster OTUs and pick representative sequences.

* 16srrna_filter.pl - Filter FASTQ files.

* 16srrna_krona.pl - Create Krona visualizations of OTU count tables.

* 16srrna_otu_network.pl - Create OTU networks.

* 16srrna_summary.pl - Generate summary tables and charts.

* annotate_out.pl - Create a merged, annotated OTU count table.

