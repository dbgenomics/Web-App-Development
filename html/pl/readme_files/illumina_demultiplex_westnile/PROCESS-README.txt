Illumina Demultiplex Pipeline
Author: Nick Bild
Date: 2016-09-28
Version 1.0: Initial development.

Description
--------

The Illumina Demultiplex Pipeline will demultiplex and convert BCL files into FASTQ files, and will rename the files to the GSL v1 format, and transfer the renamed files to marburg for further analysis.

Script relationships:


demux_bcl2fastq.pl
|
-- demux_rename.pl

Dependencies
--------

Perl v5 is required.  bcl2fastq must be installed in /opt/.

Software installed on westnile (192.168.0.6) in /home/act/software/nickbild/.

Usage Instructions
--------

The Illumina Demultiplex Pipeline is available as the "demux" pipeline.  The following steps are available (note that step numbers may change over time):

1. convert bcl to fastq
2. rename and transfer fastq files

- convert bcl to fastq

This step will ensure that there is sufficient free disk space to perform the FASTQ conversion, convert the BCL files, and check if the conversion appears to have been successful.

The following questions will be asked:

* Enter the full path to the run folder:

This is the root of the run folder, e.g.: /westnile/cluster/demultiplexing/160921_NB501676_0001_AHNMV2BGXY/

* Enter the sample sheet name, including the full path:

This is optional, but if not supplied, bcl2fastq will not know which sample to assign each read to.

Output:

<PROJ_DIR>/fastq/					-- FASTQ files.

- rename and transfer fastq files

This step will rename the FASTQ files to a GSL v1 format as it trnsfers them to marburg.  It will first check if there is enough free space available at the destination before initiaing the transfer.

The following questions will be asked:

* Enter the full path to the directory on marburg where the FASTQ files should be copied (make sure remote folder exists!):

This folder must exist somewhere under /storage01/ or /home/act/data/.

* Enter the sample sheet name, including the full path:

This is needed to assign flowcell IDs to samples.  The "Description" column of is treated as the flowcell ID.

Output:

Renamed FASTQ files at the destination specified on marburg.

Scripts
--------

* demux_bcl2fastq.pl - Convert BCL files to FASTQ files.

* demux_rename.pl - Rename FASTQ files and transfer to marburg.

