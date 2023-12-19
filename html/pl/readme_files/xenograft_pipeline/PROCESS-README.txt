Xenograft Pipeline
Author: Nick Bild
Date: 2015-08-12
Version 1.0: Initial development.
Date: 2016-03-21
Version 1.1: Port to marburg (from westnile) and convert from config file based pipeline to tophatanalysis2 format pipeline.

Description
--------
The Xenograft Pipeline aligns sequences to both human and mouse genomes.  Any sequences that aligned to both genomes are then aligned a second time with more strict alignment parameters to determine which species the sequences belong to.  A combined report giving statistics for all samples is generated.

Script relationships:

gen_cfg.pl
|
-- xenograft_step2.pl
|  |
|  -- tophat_xenograft.pl
|     |
|     -- compare_sam.pl
|     |
|     -- merge_bam.pl
|
-- xenograft_step3.pl
   |
   -- xenograft_final.pl

Dependencies
--------

Perl v5 is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/xenograft.

Usage Instructions
--------

* The pipline is available as part of the tophatanalysis2 pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

1. fastq split and qc
2. fastq filter and trim		(OPTIONAL)
4. estimate pair dist			(For species, use the target organism, "hsa")
35. xenograft human/mouse align		(For species, use "xeno")
36. xenograft reporting			(For species, use "xeno")

The steps are ran in the order that they appear above.  Unless it is explicitly stated that a step is optional, it is required for proper function of the pipeline.

Step 35 (xenograft human/mouse align) will create a "tophat" folder in the current working directory.  It will contain a subfolder for each split sample.  Each subfolder contains these files:

accepted_hits_human_1st.bam - The first pass alignments to the human genome.
accepted_hits_human_2nd.bam - The second pass alignments to the human genome.
accepted_hits_human-and-accepted_hits_mouse_1st.bam - Sequences that mapped to both human and mouse after the first pass.
accepted_hits_human-and-accepted_hits_mouse_1st.sam - Sequences that mapped to both human and mouse after the first pass.
accepted_hits_human-and-accepted_hits_mouse.bam.final.bam - Sequences that mapped to both human and mouse after the second pass.
accepted_hits_human.only_1st.bam - Sequences that mapped uniquely to human after the first pass.
accepted_hits_human.only_1st.sam - Sequences that mapped uniquely to human after the first pass.
accepted_hits_human.only.sam.final.bam - Sequences that mapped uniquely to human from the first and second pass combined.
accepted_hits_mouse_1st.bam - The first pass alignments to the mouse genome.
accepted_hits_mouse_2nd.bam - The second pass alignments to the mouse genome.
accepted_hits_mouse.only_1st.bam - Sequences that mapped uniquely to mouse after the first pass.
accepted_hits_mouse.only_1st.sam - Sequences that mapped uniquely to mouse after the first pass.
accepted_hits_mouse.only.sam.final.bam - Sequences that mapped uniquely to mouse from the first and second pass combined.
compare_sam_report.final.txt - Number of uniquely mapped tags in each category, and for each pass.

Step 36 (xenograft reporting) will create a "final" folder in the current working directory.  It will contain a subfolder for each sample.  Each sample folder will contain these files:

report.final.txt - Number of uniquely mapped tags in each category, and for each pass, for the entire sample.
both.final.bam - All mappings for the sample that could not be uniquely assigned to one organism.
human.final.bam - All unique human mappings for the sample.
mouse.final.bam - All unique mouse mappings for the sample.

The "final" folder will also contain:

xenograph-parsing-result.txt - Combined report, containing the number of uniquely mapped tags in each category, and for each pass, for all the samples.

Scripts
--------

* gen_cfg.pl - Convert westnile config file based pipeline to tophatanalysis2 format.  Silently builds config files this pipeline needs from normal tophatanalysis2 pipeline user interaction.

* xenograft_step2.pl - Launch alignment jobs.

* tophat_xenograft.pl - Align xenograft sequences to human and mouse.  Find sequences that mapped to both organisms, then align them to human and mouse again with more strict alignment parameters to find the organism they belong to.

* compare_sam.pl - Find sequencing header tags that are unique to one of the input files, or common to both.

* merge_bam.pl - Merge BAM files from 1st and 2nd alignment passes.

* xenograft_step3.pl - Launch final reporting job.

* xenograft_final.pl - Collect data from split samples, and process into a combined sample-level report.

