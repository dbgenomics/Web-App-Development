Sort and Rename + Filter File
Author: Nick Bild
Date: 2016-07-07
Version 1.0: Initial development.

Description
--------

The Sort and Rename File tool sorts tab-delimited files by row and column.  It also removes and renames columns as specified.  After all sorting and inversions have been completed, the file will be filtered according to user-defined criteria.

Script relationships:

form.html
|
-- run_program.cgi
   |
   -- sort_and_rename.pl

Dependencies
--------

Perl v5 is required.

Software installed on yonggan-Precision-WorkStation-T5400 (192.168.0.16) in /home/yonggan/www/pl/sort_and_rename_filter.

Usage Instructions
--------

* The tool is available via the ORB Intranet:

http://192.168.0.16/

Miscellaneous Utilities -> Sort and Rename + Filtering

The following questions will be asked:

- Filtering logic (for multiple criteria):
Select "AND" or "OR".

- Select data file:
Select local file or marburg file.

- Select sort order spec file:
Select local file, marburg file, or paste in a file.

The data file must be tab-delimited, and there must be a single header row positioned in the first row.

The sort order spec file must be a tab-delimited text file.  It must contain a header row, and have the 6 columns:

Column Name
Column Order
New Column Name
New Column Order
Row Sorting (Min)
Inversion
Filter criteria
Filter Operator

* "Column Name" values must match the header names in the data file.
* Rows will be sorted by the minimum value in the data across all "Row Sorting (Min)" columns marked with an "X".
* Values will be inverted (1/x) in all "Inversion" columns marked with an "X".
* Columns will be sorted and renamed by the "New Column Order" and "New Column Name" columns, respectively.
  If no value is provided for "New Column Order", the column will be omitted from the output.
* Filter criteria -contains a number or text in the row corresponding to a data column that should be used for filtering the data file.
* Filter Operator contains a ">", "<", or "=" sign in the same rows as those containing a criteria. It tells the script how to filter the data based on the criteria.
* NOTE: Filtering is the last step in the process.  It occurs after any value inversions.

A sample sort order spec file is found in the same directory as this file, named "sort_order_spec_sample.txt".

Scripts
--------

* form.html - Collects parameters from user.

* run_program.cgi - Processes user input, sets up environment, calls sort_and_rename.pl, and reports results.

* sort_and_rename.pl - Sorts file, and renames columns according to user input.  Filters data as a last step.

