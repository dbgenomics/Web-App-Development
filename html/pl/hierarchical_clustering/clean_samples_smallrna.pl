#!/usr/bin/perl
####
# Nick Bild
# 2016-09-13
# Clean small RNA sample name headers to only contain sample name.
####

$datafile = $ARGV[0];
$sampleinfo = $ARGV[1];

$replaced = 0;

# Get all sample names.
%samples = ();
open (INFILE, $sampleinfo) or die $!;
while ($row = <INFILE>) {
	$row =~ s/\n//g;
	$row =~ s/\r//g;
	@rowAry = split (/\t/, $row);

	$samples{$rowAry[0]} = 1;
}
close (INFILE);

# Clean data file.
$firsttime = 1;
open (INFILE, $datafile) or die $!;
open (OUTFILE, ">" . $datafile . ".fixheaders.txt") or die $!;
while ($row = <INFILE>) {
        $row =~ s/\n//g;
        $row =~ s/\r//g;
        @rowAry = split (/\t/, $row);

	# Header.
	if ($firsttime) {
		$firsttime = 0;
		print OUTFILE $rowAry[0];
		for ($i=1; $i<@rowAry; $i++) {
			# If column begins with "<SAMPLENAME>_", then set it to just <SAMPLENAME>.
			if ($rowAry[$i] =~ /_/) {
				@temp = split (/_/, $rowAry[$i]);
				if (exists $samples{$temp[0]}) {
					$replaced = 1;
					$rowAry[$i] = $temp[0];
				}
			}
			print OUTFILE "\t" . $rowAry[$i];
		}
		print OUTFILE "\n";
		next;
	}

	# Print remaining rows unchanged.
	print OUTFILE $row . "\n";
}
close (INFILE);
close (OUTFILE);

