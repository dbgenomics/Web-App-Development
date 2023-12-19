DESeq2
Author: Nick Bild
Date: 2017-10-30
Version 1.0: Initial development.
2017-10-31 NAB
Add option for 1 factor with pairing variable.

Description
--------------------------------------------------------------------------------

The DESeq2 pipeline will perform differential expression analyses on raw count expression data files.


Script relationships:

deseq2_run.pl

Dependencies
--------------------------------------------------------------------------------

Perl v5 is required. R 3.2.2 is required.  Required R libraries:

DESeq2
magrittr

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/.

Usage Instructions
--------------------------------------------------------------------------------

* The pipeline is available as part of statanalysis (note that step numbers may change over time):

18. deseq2

The following questions will be asked:

* Enter the name of the raw counts file (including full path, e.g.: /path/to/file.txt):

Tab-delimited file with expression data.  Sample names in header row must match
sample names in sampleinfo file. The data file can contain extra samples. Only
samples found in both the data file and the sample information file will be
used for analysis. The data file may contain annotation columns.
The gene ID must be in column 1.

Sampleinfo
--------------------------------------------------------------------------------

Tab-delimited file containing sample group information.

Column 1 of the sample information file must contain the sample names that
appear in the header row of the data file.

The analysis may have 1 or 2 factors, in column 6, and optionally, column 7.  Each factor may contain
any nmumber of levels.

If running a 1 factor analysis, a pairing variable can optionally be supplied.  In this case, factor 1
must be in column 6, and column 9 contains the pairing variable.  Columns 7 and 8 should contain "NA".

Output
--------------------------------------------------------------------------------

* 1 factor

<PROJ_DIR>/deseq2/deseq_output_1-factor_final.txt				-- Final DESeq2 output.
<PROJ_DIR>/deseq2/deseq_sizefactors_1-factor.txt				-- DESeq2 size factors.
<PROJ_DIR>/deseq2/deseq_sizefactors_overall.txt					-- DESeq2 size factors for the overall effect (if >2 levels).
<PROJ_DIR>/deseq2/deseq_output_<NUMBER>.txt					-- Intermediate file used to build final output.
<PROJ_DIR>/deseq2/deseq_output_overall.txt					-- Intermediate file used to build final output.

* 1 factor with a pairing variable

<PROJ_DIR>/deseq2//deseq_output_1factor-pairing_final.txt                        -- Final DESeq2 output.
<PROJ_DIR>/deseq2/deseq_output_1factor-pairing_<NUMBER>.txt                      -- Intermediate file used to build final output.
<PROJ_DIR>/deseq2/deseq_sizefactors_1factor-pairing.txt                          -- DESeq2 size factors.

* 2 factors

If both factors have exactly 2 levels:

<PROJ_DIR>/deseq2//deseq_output_2factor-2level_final.txt			-- Final DESeq2 output.
<PROJ_DIR>/deseq2/deseq_output_2factor-2level_<NUMBER>.txt			-- Intermediate file used to build final output.
<PROJ_DIR>/deseq2/deseq_sizefactors_2factor-2level.txt				-- DESeq2 size factors.

If one, or both, factors have >2 levels:

<PROJ_DIR>/deseq2/deseq_output_2factor-gt-2level_final.txt			-- Final DESeq2 output.
<PROJ_DIR>/deseq2/deseq_output_2factor-gt-2level_$cnt.txt			-- Intermediate file used to build final output.
<PROJ_DIR>/deseq2/deseq_sizefactors_2factor-gt-2level.txt			-- DESeq2 size factors.

Scripts
--------------------------------------------------------------------------------

* deseq2_run.pl - Collect user input, generate R code, run DESeq2, and prepare final output.

