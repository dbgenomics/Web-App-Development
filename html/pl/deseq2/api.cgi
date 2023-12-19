#!/usr/bin/perl
use CGI qw/:standard/;

print "Content-type: text/html\n\n";

# Get form data.
%para = ();
@tmp=("datafile","marburgfile", "sampleinfofile", "sampleinfomarburg", "cntfmt"); 
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

	$datafile_path = "/home/yonggan/www/pl/deseq2/$unique";
}

# Upload the sampleinfo file.
if (not $para{"sampleinfomarburg"} eq "") {
	@temp = split (/\//, $para{"sampleinfomarburg"});
        $fileonly = $temp[-1];
        system ("scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:" . $para{"sampleinfomarburg"} . " ./$unique/$fileonly");
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
	$sampleinfofile_path = "/home/yonggan/www/pl/deseq2/$unique";
}

$sampleinfo = $para{"sampleinfofile"};
$datafile = $para{"datafile"};
$cntfmt = $para{"cntfmt"};

open (LOG, ">./$unique/settings.txt") or die $!;
print LOG "Parameter\tSetting\n";
print LOG "Output Count Format:\t$cntfmt\n";
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
$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'mkdir -p /home/act/software/nickbild/webdata/deseq2/$unique'`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$sampleinfo act\@10.1.10.25:/home/act/software/nickbild/webdata/deseq2/$unique/`;
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick ./$unique/$datafile act\@10.1.10.25:/home/act/software/nickbild/webdata/deseq2/$unique/`;

# Launch the job on marburg.
system ("ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'cd /home/act/software/nickbild/webdata/deseq2/$unique; /home/act/software/nickbild/deseq2_run.pl \"$sampleinfo\" 0 \"$datafile\" \"$cntfmt\" \"compute1.q\" > /dev/null 2> /dev/null < /dev/null &'");

# Log marburg command and result
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

