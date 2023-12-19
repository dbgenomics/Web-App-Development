Usage: multiple_linear_regression_with_random_factor.R [options] EXPRDATA INFO

Run a multiple linear regression with one numeric variable and one categorical
variable and a random slope for the numeric variable.

This analysis assess how the change in gene expression relative to the numeric
variable changes with the different levels of the categorical factors.  In
addition, a random slope of the numeric variable is utilized.  The results will
be written to standard output by default.

Arguments:
    EXPRDATA
        Expression data in tab-delimited format. The first column must contain
        the gene (or microRNA, probe set, etc.) identifier. The first row must
        be a header that contains all of the sample identifiers as INFO.
    INFO
        Sample group information in tab-delimited format. The first column must
        contain sample identifiers. The numeric factor and categorical factors
        are inferred from columns 6, 7, and 8 and the variable in column 9 must
        be the random factor.

Options:
    -h --help
        Show this help message
    -d --debug
        Only run analysis on 50 randomly selected genes
    --input-is-log2
        This option indicates the data from EXPRDATA are already
        log2-transformed and therefore no transformation will be done on them
        prior to analysis.
    -o --out RESULTS
        Save results to RESULTS instead of stdout.
    -v --verbose
        Print messages on the processing steps to stderr.
