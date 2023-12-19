Annotation Generation Workflow
Author: Nick Bild
Date: 2016-05-17
Version 1.0: Initial development.

Description
--------

The Annotation Generation Workflow generates the annotation files needed for the tophatanalysis2 pipeline.

Script relationships:

parse_exons.pl
|
-- gen_sql.pl

parse_genes.pl
|
-- gen_sql.p

gen_mart_export.pl
|
-- mart_dedupe.pl

exon_len.pl

gene_len.pl

Dependencies
--------

Perl v5 is required.  No additional modules are required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

The beginning point is an appropriate GTF file downloaded from Ensembl (in the example to follow, "Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf").

NOTE: All needed data to produce Sus_scrofa 10.2 e84 annotation is provided in this folder as an example.

* Gather all needed data:
In the next step, parse_exons.pl will expect these files:

- genecoords.txt

Format:
Ensembl Gene ID	Gene Start (bp)	Gene End (bp)

- exon2proteinid.txt

Format:
Ensembl Exon ID	Ensembl Protein ID

- gene2desc.txt

Format:
Ensembl Gene ID	Description

These must be generated with BioMart to fill in annotation data not present in the GTF.  Supply the file names as parameters to parse_exons.pl as shown below.

* Add protein ids to GTF:
/home/act/software/nickbild/add_protein_ids_to_gtf.pl exon2proteinid.txt Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf > Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.gtf

* Only include autosomes, X, Y, and M:
/home/act/software/nickbild/filter_chromosomes.pl Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.gtf > Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.filter-chr.gtf

* Generate the SQL statements needed for database annotation:
/home/act/software/nickbild/parse_exons.pl gene2desc.txt genecoords.txt exon2proteinid.txt Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.filter-chr.gtf > exons.txt
/home/act/software/nickbild/parse_genes.pl exons.txt > genes.txt
* modify gen_sql.pl for genes or exons, and set appropriate tables name before each of the next 2 commands:
/home/act/software/nickbild/gen_sql.pl exons.txt > exons.sql
/home/act/software/nickbild/gen_sql.pl genes.txt > genes.sql

* Log into mysql, issue commands:
use biomart;
create table mart84_export_scr3 select * from mart66_export_hsa37 limit 0;
create table mart84_export_scr3_gene select * from mart66_export_hsa37_gene limit 0;
alter table mart84_export_scr3 add primary key (EnsemblExonID);
alter table mart84_export_scr3_gene add primary key (EnsemblGeneID);
ALTER TABLE mart84_export_scr3 MODIFY EnsemblProteinID varchar(500);
ALTER TABLE mart84_export_scr3_gene MODIFY EnsemblProteinID varchar(500);
insert into mart84_export_scr3_gene (EnsemblGeneID, ChromosomeName, GeneStartbp  , GeneEndbp  , Strand, AssociatedGeneName, Description, EnsemblExonID, ExonChrStartbp, ExonChrEndbp, ExonRankInTranscript, Biotype, EnsemblProteinID) values ("Ensembl Gene ID", "Chromosome Name", "Gene Start (bp)", "Gene End (bp)", "Strand", "Associated Gene Name", "Description", "Ensembl Exon ID", "Exon Chr Start (bp)", "Exon Chr End (bp)", "Exon Rank", "Biotype", "Ensembl Protein ID");
insert into mart84_export_scr3 (EnsemblGeneID, ChromosomeName, GeneStartbp  , GeneEndbp  , Strand, AssociatedGeneName, Description, EnsemblExonID, ExonChrStartbp, ExonChrEndbp, ExonRankInTranscript, Biotype, EnsemblProteinID) values ("Ensembl Gene ID", "Chromosome Name", "Gene Start (bp)", "Gene End (bp)", "Strand", "Associated Gene Name", "Description", "Ensembl Exon ID", "Exon Chr Start (bp)", "Exon Chr End (bp)", "Exon Rank", "Biotype", "Ensembl Protein ID");

* From the command line (this inserts the data into the database. Enter database password when prompted):
mysql -u root -p < genes.sql
mysql -u root -p < exons.sql

* Generate ANNO_NOMIT_GENE and ANNO_BIOMART_GENE files:
/home/act/software/nickbild/gen_mart_export.pl exons.txt > mart84_export_scr3.txt
# The next script sorts the mart file by chromosome, then Ensembl Gene ID.  The output file is <inputfile>.sort
/home/act/software/nickbild/sort_mart_export.pl mart84_export_scr3.txt
mv mart84_export_scr3.txt.sort mart84_export_scr3.txt
/home/act/software/nickbild/generate_noprotein_nomit_file.pl mart84_export_scr3.txt > mart84_export_scr3_nuclear_protein_coding.txt
/home/act/software/nickbild/generate_noprotein_nomit_list.pl mart84_export_scr3_nuclear_protein_coding.txt > mart84_export_scr3_nuclear_protein_coding_list.txt
** DW Comment - 2016-05-19 - The first script, gen_mart_export.pl, generates a tab-delimited file used for annotation of data with the non-sql method of the tophatanalysis2 pipeline. The second script,  easyrnaseq_noprotein_nomit_protein-not-empty.pl, generates a file with a name like mart84_export_scr3_noprotein_nomit.txt that is used by Dr. Doyles Normalization script of tophatanalysis2. This second script filters the annotation file to retain exon entries only for genes located on autosomes or sex chromosomes and only genes having one or more exons asociated with a protein ID.
** NAB 2016 UPDATE: The second script is now generate_noprotein_nomit_file.pl.

* Generate client annotation file (Remove "exon rank" column and dedupe):
/home/act/software/nickbild/mart_dedupe.pl mart84_export_scr3.txt > mart84_export_scr3_client.txt

* Calculate gene and exon lengths:

/home/act/software/nickbild/gene_len.pl Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.filter-chr.gtf > Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.lengths
/home/act/software/nickbild/exon_len.pl Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.protein-ids.filter-chr.gtf > Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.exon.lengths

* Build easyRNASeq RDA:

You'll need a small BAM file, aligned to the target genome, to continue.  If you don't have one, use an index you just built to generate one.

Next, modify this R code to fit the present genome:

--------------------------------
library(easyRNASeq)
library(BSgenome.Sscrofa.UCSC.susScr3)
setwd("/home/act/datatest/2016-04-28_sus-scrofa-test")
rnaSeq=easyRNASeq(filesDirectory="/home/act/datatest/2016-04-28_sus-scrofa-test/bam",
                                organism="Sscrofa",
                                chr.sizes="auto",
                                readLength=50L,
                                annotationMethod="gtf",
                                annotationFile="/home/act/database/sus/easyrnaseq/Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf",
                                format="bam",
                                outputFormat="RNAseq",
                                gapped=TRUE,#for tophat bam
                                normalize=TRUE,
                                filenames=c("SL139832.bam"),
                                count="genes",
                                nbCore=1,
                                summarization="geneModels",
                                validity.check=FALSE
                                )

# Build the RDA
gAnnot <- genomicAnnotation(rnaSeq)
save(gAnnot,file="gAnnot_Sscrofa10.2.ensembl84.rda")
--------------------------------

Save it to a file, and run it:

R CMD BATCH genrda.R

* Make gene and exon lengths available for RDA:
ln -s Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.exon.lengths gAnnot_Sscrofa10.2.ensembl84.rda.exon.lengths
ln -s Sus_scrofa.Sscrofa10.2.84.chr.gtf.edit.gtf.lengths gAnnot_Sscrofa10.2.ensembl84.rda.lengths

Scripts
--------

* parse_exons.pl - Parse needed data out of GTF and supplemental data files for exon annotation.

* parse_genes.pl - Parse needed data out of GTF and supplemental data files for gene annotation.

* gen_sql.pl - Prepare SQL statements to insert annotation data into database.

* gen_mart_export.pl - Generate ANNO_NOMIT_GENE and ANNO_BIOMART_GENE files.

* exon_len.pl - Calculate length of all exons.

* gene_len.pl - Calculate length of all genes.

* mart_dedupe.pl - Generate client version of mart file.  Remove "exon rank" column and dedupe.

* filter_chromosomes.pl - Filter out chromosomes other than autosomes, X, Y, or M.

* add_protein_ids_to_gtf.pl - Add protein IDs to GTF file.

