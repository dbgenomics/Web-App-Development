#!/usr/bin/perl
use CGI qw/:standard/;
use DateTime;

# Generate a timestamp.
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year = $year + 1900;
$mon++;
if ($mon < 10) { $mon = "0" . $mon; }
if ($mday < 10) { $mday = "0" . $mday; }
$timestamp = "$year-$mon-$mday $hour:$min";


print "Content-type: text/html\n\n";

# Get form data.
%para = ();
@tmp=("datafile","marburgfile", "sampleinfofile", "sampleinfomarburg", "sampleinfopaste", "headercols", "annotcols", "log2yn", "filtercols", "filterval", "thresholdpaste", "thresholdval", "contrast", "criteria", "projdesc", "feature", "datatype", "sampcluster", "reportprefix", "thresholdmarburg", "hide_gene_names", "genelist", "genelistpaste", "genelist_col");
foreach (@tmp){
	if (param($_) eq "") {
                $para{$_}=".";
        } else {
                $para{$_}=param($_);
        }
}

# Generate unique directory name.
@chars = ("A".."Z", "a".."z");
$unique .= $chars[rand @chars] for 1..8;
$unique = "webdata/$unique";

system ("mkdir -p ./$unique");

# Upload the data file.
if (not $para{"marburgfile"} eq ".") {
	@temp = split (/\//, $para{"marburgfile"});
        $fileonly = $temp[-1];

        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:" . $para{"marburgfile"} . " ./$unique/$fileonly");
        $para{"datafile"} = $fileonly;

	$datafile_path = $para{"marburgfile"};
        $datafile_path =~ s/\/$fileonly$//;
} else {
        my $filename = $para{"datafile"};
        my $output_file = "/tmp/uploaded";
        my ($bytesread, $buffer);
        my $numbytes = 1024;
        open (OUT, ">./$unique/" . $para{"datafile"});
        while ($bytesread = read($filename, $buffer, $numbytes)) {
                print OUT $buffer;
        }
        close OUT;

	$datafile_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";
}

# Upload the sampleinfo file.
if (not $para{"sampleinfomarburg"} eq ".") {
	@temp = split (/\//, $para{"sampleinfomarburg"});
        $fileonly = $temp[-1];

        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:" . $para{"sampleinfomarburg"} . " ./$unique/$fileonly");
        $para{"sampleinfofile"} = $fileonly;

	$sampleinfofile_path = $para{"sampleinfomarburg"};
        $sampleinfofile_path =~ s/\/$fileonly$//;

} elsif (not $para{"sampleinfopaste"} eq ".") {
        open (OUTFILE, ">./$unique/sampleinfo.txt") or die $!;
        print OUTFILE $para{"sampleinfopaste"};
        close (OUTFILE);
        $para{"sampleinfofile"} = "sampleinfo.txt";

	$sampleinfofile_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";
} else {
        my $filename = $para{"sampleinfofile"};
        my $output_file = "/tmp/uploaded";
        my ($bytesread, $buffer);
        my $numbytes = 1024;
        open (OUT, ">./$unique/" . $para{"sampleinfofile"});
        while ($bytesread = read($filename, $buffer, $numbytes)) {
                print OUT $buffer;
        }
        close OUT;

	$sampleinfofile_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";
}

# Upload genelist
if (not $para{"genelistpaste"} eq ".") {
        open (OUTFILE, ">./$unique/genelist.txt") or die $!;
        print OUTFILE $para{"genelistpaste"};
        close (OUTFILE);
        $para{"genelist"} = "genelist.txt";

        $genelist_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";
} elsif (not $para{"genelist"} eq ".") {
        my $filename = $para{"genelist"};
        my $output_file = "/tmp/uploaded";
        my ($bytesread, $buffer);
        my $numbytes = 1024;
        open (OUT, ">./$unique/" . $para{"genelist"});
        while ($bytesread = read($filename, $buffer, $numbytes)) {
                print OUT $buffer;
        }
        close OUT;

        $genelist_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";
}

# Create the threshold file, if data supplied.
if (not $para{"thresholdval"} eq ".") {
	if (not $para{"thresholdmarburg"} eq ".") {
       		system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:" . $para{"thresholdmarburg"} . " ./$unique/threshold.txt");
	} else {
        	open (OUTFILE, ">./$unique/threshold.txt") or die $!;
        	print OUTFILE $para{"thresholdpaste"};
        	close (OUTFILE);
	}
}
$thresholds_path = "/home/yonggan/www/pl/hierarchical_clustering/$unique";

$sampleinfo = $para{"sampleinfofile"};
$datafile = $para{"datafile"};
$headercols = $para{"headercols"};
$annotcols = $para{"annotcols"};
$log2yn = $para{"log2yn"};
$filtercols = $para{"filtercols"};
$filterval = $para{"filterval"};
$thresholdval = $para{"thresholdval"};
$contrast = $para{"contrast"};
$criteria = $para{"criteria"};
$projdesc = $para{"projdesc"};
$feature = $para{"feature"};
$datatype = $para{"datatype"};
$sampcluster = $para{"sampcluster"};
$reportprefix = $para{"reportprefix"};
$hide_gene_names = $para{"hide_gene_names"};
$genelist = $para{"genelist"};
$genelist_col = $para{"genelist_col"};

# NAB 2017-01-04: Check that sampleinfo file contains all sample renaming fields, and that all names are unique.
%unq_samples = ();
%sample_map = ();
if (not $headercols eq ".") {
	open (INFO, "./$unique/$sampleinfo") or die $!;
	while ($row = <INFO>) {
		if ($row =~ /^\#/) { next; }
		$row =~ s/\n//g;
		$row =~ s/\r//g;
		@rowAry = split (/\t/, $row);

		@vals = split (/,/, $headercols);
		$sample_name = "";
		foreach $val (@vals) {
			$val--; # 0-based counting.

			if ($rowAry[$val] eq "") {
				$val++; # 1-based counting for user.
				print "ERROR: Sample naming column '$val' in the sampleinfo file is not defined! Click back to fix.";
				die;
			}
			$sample_name .= $rowAry[$val] . "_";
		}
		$sample_name =~ s/_$//;

		$sample_map{$rowAry[0]} = $sample_name;

		if (exists $unq_samples{$sample_name}) {
			print "ERROR: sample name '$sample_name' is not unique in sampleinfo file!  Click back to fix.";
			die;
		}

		$unq_samples{$sample_name} = 1;
	}
	close (INFO);
}

# NAB 2017-05-18: Store renamed samples for displaying to user.
open (OUTSAMPLE, ">./$unique/sample_names.txt") or die $!;
for $sample (sort keys %sample_map) {
	print OUTSAMPLE $sample . "\t" . $sample_map{$sample} . "\n";
}
close (OUTSAMPLE);

# NAB 2016-09-13: Clean the sample names in the data file (esp. for small RNA).
system ("/home/yonggan/www/pl/pca/clean_samples_smallrna.pl ./$unique/$datafile ./$unique/$sampleinfo");
# KKO 2016-12-20: Keep a record of the input datafile
$datafile_org = $datafile;
$datafile = $datafile . ".fixheaders.txt";

open (LOG, ">./$unique/settings.txt") or die $!;
print LOG "Parameter\tSetting\n";

print LOG "Which columns in the sampleinfo file should be combined to name the samples? $headercols\n";
print LOG "Which annotation columns should be combined to create a new gene id? $annotcols\n";
print LOG "Is the data log transformed? $log2yn\n";
print LOG "Do you want to cluster by samples? $sampcluster \n";
print LOG "Do you want to filter the data? If yes, enter the columns to filter: $filtercols\n";
print LOG "If filtering, what is your filtering cutoff value (e.g. 0.05)? 1+ genes in filter columns must be < this value to be retained. $filterval\n";
print LOG "Filter Gene List: $genelist\n";
print LOG "Description of filtering criteria: $criteria\n";
print LOG "Report Subtitle: $projdesc\n";
print LOG "Report Name: $reportprefix\n";
print LOG "Feature type? $feature\n";
print LOG "Data Type? $datatype\n";

print LOG "-----------------------\n";
print LOG "File\tType\tPath\tModification Time\tMD5 Checksum\n";

$md5_val = md5("./$unique/$datafile_org");
if ($datafile_path =~ m%/yonggan/%) {
	$mod_val = mod("$datafile_path/$datafile_org");
} else {
	$mod_val = mod_marburg("$datafile_path/$datafile_org");
}
print LOG join("\t", $datafile_org, "Input Data File", $datafile_path, $mod_val, $md5_val), "\n";

$md5_val = `md5sum ./$unique/$datafile`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
if ($datafile_path =~ /\/yonggan\//) {
        $mod_val = mod("$datafile_path/$datafile");
} else {
        $mod_val = mod_marburg("$datafile_path/$datafile");
}
print LOG "$datafile\tData File With Sample Names Corrected\t$datafile_path\t$mod_val\t$md5_val\n";

$md5_val = `md5sum ./$unique/$sampleinfo`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
if ($sampleinfofile_path =~ /\/yonggan\//) {
        $mod_val = mod("$sampleinfofile_path/$sampleinfo");
} else {
        $mod_val = mod_marburg("$sampleinfofile_path/$sampleinfo");
}
print LOG "$sampleinfo\tSample Info File\t$sampleinfofile_path\t$mod_val\t$md5_val\n";

$md5_val = `md5sum ./$unique/threshold.txt`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
$mod_val = mod("./$unique/threshold.txt");
print LOG "threshold.txt\tThreshold File\t/home/yonggan/www/pl/hierarchical_clustering/$unique\t$mod_val\t$md5_val\n";
close (LOG);

# Save settings.
open (OUTFILE, ">./$unique/about.txt") or die $!;
print OUTFILE $timestamp . "\n";
print OUTFILE "Sample Info: $sampleinfo\n";
print OUTFILE "Original Input Data File: $datafile_org\n";
print OUTFILE "Data File: $datafile\n";
print OUTFILE "Which columns in the sampleinfo file should be combined to name the samples? $headercols\n";
print OUTFILE "Which annotation columns should be combined to create a new gene id? $annotcols\n";
print OUTFILE "Is the data log transformed? $log2yn\n";
print OUTFILE "Do you want to cluster by samples? $sampcluster \n";
print OUTFILE "Do you want to filter the data? If yes, enter the columns to filter: $filtercols\n";
print OUTFILE "If filtering, what is your filtering cutoff value (e.g. 0.05)? 1+ genes in filter columns must be < this value to be retained. $filterval\n";
print OUTFILE "Filter Gene List: $genelist\n";
print OUTFILE "Description of filtering criteria: $criteria\n";
print OUTFILE "Report Subtitle: $projdesc\n";
print OUTFILE "Report Name: $reportprefix\n";
print OUTFILE "Feature type? $feature\n";
print OUTFILE "Data Type? $datatype\n";
close (OUTFILE);

# Determine first data column.
%samples = ();
open (INFILE, "./$unique/" . $sampleinfo) or die $!;
while ($row = <INFILE>) {
        if ($row =~ /^\#/) { next; }
        $row =~ s/\n//g;
        $row =~ s/\r//g;
        @rowAry = split (/\t/, $row);

        $samples{$rowAry[0]} = 1;
}
close (INFILE);

$datacol = -1;
$firsttime = 1;
open (INFILE, "./$unique/" . $datafile) or die $!;
while ($row = <INFILE>) {
        $row =~ s/\n//g;
        $row =~ s/\r//g;
        @rowAry = split (/\t/, $row);

        if ($firsttime) {
                $firsttime = 0;
                for ($i=0; $i<@rowAry; $i++) {
                        if (exists $samples{$rowAry[$i]}) {
                                $datacol = $i;
                                last;
                        }
                }
        } else {
                last;
        }
}
close (INFILE);
# END - Determine first data column.

# Check to make sure data columns found.
if ($datacol == -1) {
	print "ERROR: No data columns found! Check data and sampleinfo file to be sure sample names match.  Click back to correct.  Exiting...\n";
	die;
}

# Check to make sure data appears log transformed, if user indicated it was.
if ($log2yn eq "N") {
	$firsttime = 1;
	$dataok = 1;
	open (INFILE, "./$unique/" . $datafile) or die $!;
	while ($row = <INFILE>) {
        	$row =~ s/\n//g;
        	$row =~ s/\r//g;
        	@rowAry = split (/\t/, $row);

		if ($firsttime) { $firsttime = 0; next; } # Skip the header.

		for ($i=$datacol; $i<@rowAry; $i++) {
			if ($rowAry[$i] =~ /^-/) {
				$dataok = 0;
				last;
			}
		}
	}

	if ($dataok == 0) {
		print "ERROR: You indicated that the data was log transformed, but negative values were found in the data!.  Click back to correct.  Exiting...\n";
		die;
	}
}

# Set up environment and transfer data to marburg.
$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'mkdir -p /home/act/software/nickbild/webdata/hierarchical_clustering/$unique'`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$sampleinfo act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$datafile act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/`;
if (not $genelist eq ".") {
	$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$genelist act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/`;
}

if (not $thresholdval eq ".") {
	$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/threshold.txt act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/`;
}

open (INFO, ">./$unique/extrainfo.txt") or die $!;
print INFO $criteria . "\n";
print INFO $projdesc . "\n";
print INFO $feature . "\n";
print INFO $datatype . "\n";
print INFO $log2yn . "\n";
print INFO $sampcluster . "\n";
print INFO $reportprefix . "\n";
print INFO qq{Command: ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'cd /home/act/software/nickbild/webdata/hierarchical_clustering/$unique; /home/act/software/nickbild/clustering_web.pl $sampleinfo $datafile $headercols $annotcols $log2yn $filtercols $filterval $datacol $thresholdval $sampcluster \"$reportprefix\" \"$feature\" \"$datatype\" \"$genelist\" \"$genelist_col\"'
};
close (INFO);

# Launch the job on marburg.
$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'cd /home/act/software/nickbild/webdata/hierarchical_clustering/$unique; /home/act/software/nickbild/clustering_web.pl $sampleinfo $datafile $headercols $annotcols $log2yn $filtercols $filterval $datacol $thresholdval $sampcluster \"$reportprefix\" \"$feature\" \"$datatype\" \"$genelist\" \"$genelist_col\"'`;

# Load status page.
print "<script>\n";
print "window.location = \"status.cgi?unique=$unique&contrast=$contrast&genehide=$hide_gene_names\";\n";
print "</script>\n";

sub mod {
        $mod = `stat -c %y @_`;
        @temp = split (/\./, $mod);
        $mod = $temp[0];
        return $mod;
}

sub mod_marburg {
        $mod = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 "stat -c %y @_"`;
        @temp = split (/\./, $mod);
        $mod = $temp[0];
        return $mod;
}

sub md5 {
        $md5 = `md5sum @_`;
        @temp = split (/\s+/, $md5);
        $md5 = $temp[0];
        return $md5;
}

exit;

