Barnes Hutt tSNE
Author: Nick Bild
Date: 2018-01-15
Version 1.0: Initial development.
UPDATE 2018-01-29 NAB
Add option to set perplexity.
Change number of initial dimensions from the number of genes to the number of samples, and set the maximum value to 50.

Description
--------------------------------------------------------------------------------

The Barnes Hutt tSNE aaplication will reduce the dimensionality of a gene expression data set and plot the results.

Script relationships:

bhtsne_run.pl

Dependencies
--------------------------------------------------------------------------------

Perl v5 is required. R 3.2.2 is required.  bh_tsne (https://github.com/lvdmaaten/bhtsne) is required.

Software installed on marburg (192.168.0.14) in /home/act/software/nickbild/.

Usage Instructions
--------------------------------------------------------------------------------

The application is available on ORB's intranet:

http://192.168.0.16/ -> Statistics -> Barnes-Hut tSNE

The following questions will be asked:

* Enter the plot width (in pixels):  
* Enter the plot height (in pixels):  
* Enter the plot resolution:  

These control the size and resolution of the plot jpeg generated.
 
* Include axis in plot?

Should grid lines be shown?

* Enter a font size for the plot:  

The font size for all text in the plot.

* Enter a title for the plot:

Optional.  Text to display above the plot.

* Enter the perplexity value:

From https://lvdmaaten.github.io/tsne/:

====
Perplexity is a measure for information that is defined as 2 to the power of the Shannon entropy. The perplexity of a fair die with k sides is equal to k. In t-SNE, the perplexity may be viewed as a knob that sets the number of effective nearest neighbors. It is comparable with the number of nearest neighbors k that is employed in many manifold learners.
====

* Enter the data file (including full path):

The data file is expected to be tab-delimited and have a header row as the first row.
Sample names in the header row must exactly match sample names in the sampleinfo file.
A maximum of 50,000 genes is allowed.

* Select sampleinfo file:

A standard sampleinfo file is expected, with sample names in the first column and group names in column 6-8.
If some group columns are not needed, set them to to "NA" or leave them blank.

After the run completes, the status page will allow you to regenerate the plot with different parameters, without re-running the bh_tsne software.

Output
--------------------------------------------------------------------------------

bhtsne_plot.jpg				-- Plot of Barnes Hutt tSNE output.
plot_data.txt				-- Data used to generate the plot.
bhtsne_result.txt			-- Direct Barnes Hutt tSNE output.
bhtsne_output.txt			-- Output from running Barnes Hutt tSNE software.

Scripts
--------------------------------------------------------------------------------

* bhtsne_run.pl - Collect parameters, prepare input data, run bh_tsne software, and generate plots.

