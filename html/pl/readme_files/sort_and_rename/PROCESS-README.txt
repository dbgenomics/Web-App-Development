Sort and Rename File
Author: Nick Bild
Date: 2016-04-13
Version 1.0: Initial development.
Date: 2016-06-23 NAB
Allow for file names with underscores to be used.
Remove any trailing newlines from data file to ensure proper sorting.

Description
--------

The Sort and Rename File tool sorts tab-delimited files by row and column.  It also removes and renames columns as specified.

Script relationships:

form.html
|
-- run_program.cgi
   |
   -- sort_and_rename.pl

Dependencies
--------

Perl v5 is required.

Software installed on yonggan-Precision-WorkStation-T5400 (192.168.0.16) in /home/yonggan/www/pl/sort_and_rename.

Usage Instructions
--------

* The tool is available via the ORB Intranet:

http://192.168.0.16/

Miscellaneous Utilities -> Sort and Rename File

The following questions will be asked:

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

* "Column Name" values must match the header names in the data file.
* Rows will be sorted by the minimum value in the data across all "Row Sorting (Min)" columns marked with an "X".
* Values will be inverted (1/x) in all "Inversion" columns marked with an "X".
* Columns will be sorted and renamed by the "New Column Order" and "New Column Name" columns, respectively.
  If no value is provided for "New Column Order", the column will be omitted from the output.

A sample sort order spec file is found in the same directory as this file, named "sort_order_spec_sample.txt".

Scripts
--------

* form.html - Collects parameters from user.

* run_program.cgi - Processes user input, sets up environment, calls sort_and_rename.pl, and reports results.

* sort_and_rename.pl - Sorts file, and renames columns according to user input.

