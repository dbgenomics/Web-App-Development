#!/usr/bin/perl
use CGI qw/:standard/;

print "Content-type: text/html\n\n";

# Get form data.
%para = ();
@tmp=("datafile","marburgfile", "sampleinfofile", "sampleinfomarburg", "thresholdfile", "thresholdmarburg", "log", "logt"); 
foreach (@tmp){
	$para{$_}=param($_);
}

# Generate unique directory name.
@chars = ("A".."Z", "a".."z");
$unique .= $chars[rand @chars] for 1..8;
$unique = "webdata/$unique";

system ("mkdir -p ./$unique");

# Upload the data file.
if (not $para{"marburgfile"} eq "") {
	@temp = split (/\//, $para{"marburgfile"});
        $fileonly = $temp[-1];
        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14:" . $para{"marburgfile"} . " ./$unique/$fileonly");
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

	$datafile_path = "/home/yonggan/www/pl/dunnetts_test/$unique";
}

# Upload the sampleinfo file.
if (not $para{"sampleinfomarburg"} eq "") {
	@temp = split (/\//, $para{"sampleinfomarburg"});
        $fileonly = $temp[-1];
        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14:" . $para{"sampleinfomarburg"} . " ./$unique/$fileonly");
        $para{"sampleinfofile"} = $fileonly;

	$sampleinfofile_path = $para{"sampleinfomarburg"};
        $sampleinfofile_path =~ s/\/$fileonly$//;
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
	$sampleinfofile_path = "/home/yonggan/www/pl/dunnetts_test/$unique";
}

# Upload thresholds file.
if (not $para{"thresholdmarburg"} eq "") {
        @temp = split (/\//, $para{"thresholdmarburg"});
        $fileonly = $temp[-1];
        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14:" . $para{"thresholdmarburg"} . " ./$unique/$fileonly");
        $para{"thresholdfile"} = $fileonly;

        $thresholdfile_path = $para{"thresholdmarburg"};
        $thresholdfile_path =~ s/\/$fileonly$//;
} else {
        my $filename = $para{"thresholdfile"};
        my $output_file = "/tmp/uploaded";
        my ($bytesread, $buffer);
        my $numbytes = 1024;
        open (OUT, ">./$unique/" . $para{"thresholdfile"});
        while ($bytesread = read($filename, $buffer, $numbytes)) {
                print OUT $buffer;
        }
        close OUT;
        $thresholdfile_path = "/home/yonggan/www/pl/dunnetts_test/$unique";
}

$sampleinfo = $para{"sampleinfofile"};
$datafile = $para{"datafile"};
$threshold = $para{"thresholdfile"};
$log = $para{"log"};
$logt = $para{"logt"};

open (LOG, ">./$unique/settings.txt") or die $!;
print LOG "Parameter\tSetting\n";
print LOG "Data File Log Base:\t$log\n";
print LOG "Threshold File Log Base:\t$logt\n";
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

$md5_val = `md5sum ./$unique/$threshold`;
@temp = split (/\s+/, $md5_val);
$md5_val = $temp[0];
if ($thresholdfile_path =~ /\/yonggan\//) {
        $mod_val = mod("$thresholdfile_path/$threshold");
} else {
        $mod_val = mod_marburg("$thresholdfile_path/$threshold");
}
print LOG "$threshold\t$thresholdfile_path\t$mod_val\t$md5_val\n";

# Set up environment and transfer data to marburg.
$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14 'mkdir -p /home/act/software/nickbild/webdata/dunnetts_test/$unique'`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$sampleinfo act\@192.168.0.14:/home/act/software/nickbild/webdata/dunnetts_test/$unique/`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$datafile act\@192.168.0.14:/home/act/software/nickbild/webdata/dunnetts_test/$unique/`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$threshold act\@192.168.0.14:/home/act/software/nickbild/webdata/dunnetts_test/$unique/`;

# Launch the job on marburg.
system ("ssh -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14 'cd /home/act/software/nickbild/webdata/dunnetts_test/$unique; /home/act/software/nickbild/dunnetts_test.pl \"$sampleinfo\" 0 \"$datafile\" \"$threshold\" \"$log\" \"$logt\" > /dev/null 2> /dev/null < /dev/null &'");

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
        $mod = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@192.168.0.14 "stat -c %y @_"`;
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

