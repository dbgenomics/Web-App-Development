#!/usr/bin/perl
#	by Yonggan Wu and Silke Dodel
#	yongganw@oceanridgebio.com
#	Ocean Ridge Bioscience LLC
#	Updated to accept a threshold file as input to the script
#	oap_program.txt was also updated
#	Version (2016-03-17 09:42):    Kevin K. Ogden
#		Adds validation to the isdatalog2 input to allow the user to enter
#		"true", "yes", or "y" for TRUE and
#		"false", "no", or "n" for FALSE
#		Also adds a check for existence of datafolder and datafile when the user enters them
#       Version 05 Data: 2014-02-12
#	Version 05 Updates: Include contrast in mixed effects ANOVA with unbalanced design, make fold changes options correspond to tukey test options
#	steps:
#		1) read the comparison groups
#		2) create an R code to do the statistical analysis
#	R code steps
#		1) read all input tables and threshold files
#               1A) perform regression if one or more of the fixed factors are numerical
#		2) calculate the ANOVA (1,2,3-way and fixed or mixed effects as needed)
#                  type I for balanced design
#                  type II for unbalanced design (type III with contrasts contr.sum for mixed effects analysis with unbalanced design)
#                  Correlation model in mixed effects analysis: corAR1()
#                  number of factors and type are determined automatically
#		3) calculate the tukey test
#		4) calculate the fold changes
#               5) ONLY if one or more factors are numerical:
#                  perform regresion analysis on the numerical factors
#                  Models: 
#                  a) For 1 numerical factor f1:
#                     y ~ f1
#                  b) For 2 numerical factors f1, f2:
#                     y ~ f1 + f2 + f1.f2
#                  c) For 3 numerical factors f1, f2, f3:
#                     y ~ f1 + f2 + f3 + f1.f2 + f1.f3 + f2.f3 + f1.f2.f3
#		6) merge the result and output the table
#	version 1.1 (2013-06-06 16:19:28 ): add function to change the comparision order
#	Input file: merged and filtered cufflink result
#	Output file: statistical analysis result
#	System Requirements: linux, perl, R
#	Usage: perl  
#
#  Usage: perl tophat_general_stat.pl <datafolder> <datafile> <SampleInfor> <comparison decrease order TRUE/FALSE> <tukey_options: separate/combined/conditional> <number of descriptive columns in data file> <isdatalog2: is data log2 transformed? TRUE/FALSE> <--qsub>
#
#
#  <tukey_options>: separate/combined/conditional
#
#  
# a) "separate": the Tukey test is performed for each factor separately without regard of the other factors.
# b) "conditional": the Tukey test will be performed for each factor while holding the conditions of the other factors constant.
# c) "combined": the Tukey test is performed by combining the conditions of all the factors and interpreting each combination as a condition of a combined factor.
# 
# In any case the Tukey test will be performed only, if there are three or more conditions after applying the options. 
#
# Obviously, for only one factor, the three cases will be identical.
# 
# Example: 
# Factor 1   Factor 2
# 1A         2A
# 1B         2B
# 1C         2C
#            2D
# 
# a) separate: Two Tukey tests will be performed, one on Factor 1, one on Factor 2, with each test ignoring the respective other factor.
#
# b) conditional: Tukey tests will be performed restricted to the samples with the following conditions: 
#  - 1A: all conditions of factor 2
#  - 1B:            "
#  - 1C:            "
#  - 2A: all conditions of factor 1
#  - 2B:            "
#  - 2C:            "
#  - 2D:            "
#  The number of Tukey tests performed will be at most 
#  n1 + n2 for two factors with n1 and n2 conditions, respectively, and 
#  n1*n2+n1*n3+n1*n3 for three factors with n1, n2, and n3 conditions, respectively. This yields at most n1*n2*(n2-1)/2+n2*n1*(n1-1)/2 comparisons in the two factor case and n1*n2*n3*(n3-1)/2+n1*n3*n2*(n2-1)/2+n2*n3*n1*(n1-1)/2 in the three factor case. This is an upper limit to the number of comparisons, since there might not be samples for every comparison.
#
# c) combined: One Tukey test will be performed with the following conditions:
#   1A 2A
#   1A 2B
#     .
#     .
#     .
#   1C 2D
#   The number of conditions is N=n1*n2 for two factors and N=n1*n2*n3 for three factors. The number of comparisons is at most N*(N-1)/2
#
#   UPDATE 2016-05-03 NAB: No changes.  Updating documentation for completeness.  The following questions will be asked:
#   * Please enter the name of the data folder:
#   * Please enter the name of the data file (which must be located in the jobs directory): 
#   * Please enter the tukey option you want to use (separate/combined/conditional):
#   * Please enter the number of descriptive columns in the data file . (often 8) : 
#   * Is data already log2 transformed? (TRUE/FALSE): 
#   * Please enter the name of the threshold file: (hit ENTER if you want the thresholds to be automatically generated) 
#   * Please enter the row number (treat the header as row 0) from which the thresholds are to be read.
#
#   ####  R files used to generate the target R file which is executed:
#
#   Only one file of each analysis is selected to generate the target R file. 
#   Selection is based on user defined variables (tukey_options) and variables determined from the sample information file (e.g. sample_infor_combined.txt). The extension .Rpart indicates that the files are not stand-alone R files as they depend on variables in the other .Rpart files.
# 
#   Reading input files and adjusting data arrays:
#      ReadInputFilesAdjustArrays.Rpart
# 
#   Compute combination vectors needed for Tukey test and fold changes:
#      CalculateCombinations1.Rpart
#      CalculateCombinations2.Rpart
#      CalculateCombinations3.Rpart
#
#   Regression analysis (only performed, if one or more fixed factors are numerical)
#      CalculateRegression1.Rpart 
#      CalculateRegression2.Rpart 
#      CalculateRegression3.Rpart 
#
#   ANOVA:
#      if no random factor present:
#      CalculateANOVA1.Rpart   1-way fixed effect ANOVA
#      CalculateANOVA2.Rpart   2-way
#      CalculateANOVA3.Rpart   3-way
#      if random factor present:
#      CalculateMEANOVA1.Rpart   1-way mixed effect ANOVA
#      CalculateMEANOVA2.Rpart   2-way
#      CalculateMEANOVA3.Rpart   3-way
# 
#   Tukey:
#      combined:
#        TukeySeparate.Rpart       1-way
#        TukeyCombined.Rpart       2-way and 3-way
#      conditional:
#        TukeyConditional2.Rpart   2-way
#        TukeyConditional3.Rpart   3-way
#      separate:
#        TukeySeparate.Rpart
#
#    Fold changes: (options correspond to Tukey options)
#      combined:
#        FoldChangesSeparte1.Rpart      1-way   
#        FoldChangesCombined.Rpart      2-way and 3-way
#      conditional:
#        FoldChangesConditional2.Rpart   2-way
#        FoldChangesConditional3.Rpart   3-way
#      separate:
#        FoldChangesSeparate1.Rpart  1-way
#        FoldChangesSeparate2.Rpart  2-way
#        FoldChangesSeparate3.Rpart  3-way
#
#    Regression (ONLY if one or more factors are numerical)
#        CalculateRegression1.Rpart
#        CalculateRegression2.Rpart
#        CalculateRegression3.Rpart
#
#    Order output array and write it to output file
#        WriteToOutputFile.Rpart
#  
# UPDATE 2016-03-16 NAB
# If no thresholds file is provided, one will be automatically generated.
# If supplying a thresholds file, you will also be prompted to specify the
# row number containing the thresholds.
#
# UPDATE NAB 2016-04-04 
# Add summary report and column name/number mapping.
#
# UPDATE NAB 2016-06-01
# Filter threshold file to only contain samples in sampleinfo file.
# Print warning when in "separate" mode:
# "The sampleinfo, threshold, and data file must contain the same samples when running analysis in Separate mode."
# Set Tukey values to NA if both group means below corresponding threshold means.
# Output _settings.txt file, and put same info in pipeline.log.
# Remove "order" option that was unused.
#
# UPDATE NAB 2016-06-13
# Remove 'separate' Tukey option.
#
# UPDATE NAB 2016-06-14: Halt execution if threshold file is missing any samples that are
# common between the sampleinfo and data files.
#
# UPDATE NAB 2016-06-22
# Change location of thresholds_auto.txt to $datafolder.
#
# UPDATE NAB 2016-06-23
# Modify to include a non-interactive mode for web-based use.
#
################################################################################
