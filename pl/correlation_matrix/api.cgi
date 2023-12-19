#!/usr/bin/perl
use CGI qw/:standard/;

print "Content-type: text/html\n\n";

# Get form data.
%para = ();
@tmp=("datafile","marburgfile", "sampleinfofile", "sampleinfomarburg", "sampleinfopaste", "headercols", "limits", "log2yn", "width", "height", "datacol", "cluster", "feature", "datatype", "speciessel", "criteria", "projdesc");
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

	$datafile_path = "/home/yonggan/www/pl/correlation_matrix/$unique";
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

	$sampleinfofile_path = "/home/yonggan/www/pl/correlation_matrix/$unique";
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
	$sampleinfofile_path = "/home/yonggan/www/pl/correlation_matrix/$unique";
}

$sampleinfo = $para{"sampleinfofile"};
$datafile = $para{"datafile"};
$headercols = $para{"headercols"};
$limits = $para{"limits"};
$log2yn = $para{"log2yn"};
$width = $para{"width"};
$height = $para{"height"};
$datacol = $para{"datacol"};
$cluster = $para{"cluster"};
$feature = $para{"feature"};
$datatype = $para{"datatype"};
$speciessel = $para{"speciessel"};
$criteria = $para{"criteria"};
$projdesc = $para{"projdesc"};

# NAB 2016-09-13: Clean the sample names in the data file (esp. for small RNA).
system ("/home/yonggan/www/pl/correlation_matrix/clean_samples_smallrna.pl ./$unique/$datafile ./$unique/$sampleinfo");
$datafile = $datafile . ".fixheaders.txt";

open (LOG, ">./$unique/settings.txt") or die $!;
print LOG "Parameter\tSetting\n";
print LOG "Header Columns:\t$headercols\n";
print LOG "Limits\t$limits\n";
print LOG "Log2:\t$log2yn\n";
print LOG "Width:\t$width\n";
print LOG "Height:\t$height\n";
print LOG "Data Column:\t$datacol\n";
print LOG "Cluster:\t$cluster\n";
print LOG "Feature Type:\t$feature\n";
print LOG "Data Type:\t$datatype\n";
print LOG "Species:\t$speciessel\n";
print LOG "Criteria:\t$criteria\n";
print LOG "Proj. Desc.:\t$projdesc\n";
print LOG "-----------------------\n";
print LOG "File\tPath\tModification Time\tMD5 Checksum\n";

$md5_val = `md5sum ./$unique/$datafile`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
if ($datafile_path =~ /\/yonggan\//) {
        $mod_val = mod("$datafile_path/$datafile");
} else {
        $mod_val = mod_marburg("$datafile_path/$datafile");
}
print LOG "$datafile\t$datafile_path\t$mod_val\t$md5_val\n";

$md5_val = `md5sum ./$unique/$sampleinfo`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
if ($sampleinfofile_path =~ /\/yonggan\//) {
        $mod_val = mod("$sampleinfofile_path/$sampleinfo");
} else {
        $mod_val = mod_marburg("$sampleinfofile_path/$sampleinfo");
}
print LOG "$sampleinfo\t$sampleinfofile_path\t$mod_val\t$md5_val\n";

# Set up environment and transfer data to marburg.
$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'mkdir -p /home/act/software/nickbild/webdata/correlation_matrix/$unique'`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$sampleinfo act\@10.1.10.25:/home/act/software/nickbild/webdata/correlation_matrix/$unique/`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$datafile act\@10.1.10.25:/home/act/software/nickbild/webdata/correlation_matrix/$unique/`;

# Launch the job on marburg.
$cmd = "ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'cd /home/act/software/nickbild/webdata/correlation_matrix/$unique; /home/act/software/nickbild/correlation.pl $sampleinfo 0 \"$datafile\" \"$headercols\" \"$limits\" \"$log2yn\" \"$width\" \"$height\" \"$datacol\" \"$cluster\" \"$feature\" \"$datatype\" \"$speciessel\" \"$criteria\" \"$projdesc\"'";
$var = `$cmd 2>&1`;

# Log marburg command and result
print LOG "\nMarburg command: $cmd\n";
print LOG "Response: $var", "\n";
close (LOG);

# Load status page.
print "<script>\n";
print "window.location = \"status.cgi?unique=$unique\";\n";
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

