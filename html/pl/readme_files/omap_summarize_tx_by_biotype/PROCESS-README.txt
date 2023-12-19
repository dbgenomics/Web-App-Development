OMAP Summarize Transcripts by Biotype
Author: Nick Bild
Date: 2016-03-22
Version 1.0: Initial development.

Description
--------
The OMAP Summarize Transcripts by Biotype tool produces textual summary tables and a graphical plot to visualize the data.

Script relationships:

omap_summarize_tx_by_biotype.pl
|
-- summarize_transcripts.R
|
-- plot_transcripts.R

Dependencies
--------

Perl v5 is required.  R version 3.2 is required.  The following R libraries are required:

docopt
dplyr
reshape2
ggplot2
magrittr
lazyeval

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild.

Usage Instructions
--------

* The pipline is available as part of the omap pipeline, and this is the recommended method of running the pipeline (note that step numbers may change over time):

24. summarize transcripts by biotype

The tool expects that the file "align_transcript/transcript_result_match_raw_filter.txt" in the current working directory already exists, as this will be used as input.  If not found, an error message will be displayed and the program will exit.

Output will be placed in a folder named "align_transcript" under the current working directory:

- transcript_summary_raw.txt - Transcripts by biotype, raw numbers.

- transcript_summary_percent.txt - Transcripts by biotype, as percentages.

- transcript_summary_percent.png - Graphical representation of transcripts by biotype, as percentages.

* Alternatively, to run the pipeline manually:

./omap_summarize_tx_by_biotype.pl sampleinfo.txt

Scripts
--------

* omap_summarize_tx_by_biotype.pl - Calls the R scripts with the proper parameters and in the proper sequence.  Also standardizes input and output file names. 

* summarize_transcripts.R - Script developed by Kevin Ogden to summarize transcripts by biotype, raw numbers or percentages.

* plot_transcripts.R - Script developed by Kevin Ogden to generate graphical representation of transcripts by biotype (percentages).
 
