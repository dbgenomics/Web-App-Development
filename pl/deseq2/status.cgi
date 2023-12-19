#!/usr/bin/perl
use CGI qw/:standard/;

print "Content-type: text/html\n\n";

# Get URL variables.
%para = ();
@tmp=("unique");
foreach (@tmp){
	$para{$_}=param($_);
}

$unique = $para{"unique"};

# Check to see if job has completed.
$result = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'ls /home/act/software/nickbild/webdata/deseq2/$unique/deseq2/run.finished'`;

if ($result eq "") {
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	$year = $year + 1900;
	$mon++;
	if ($mon < 10) { $mon = "0" . $mon; }
	if ($mday < 10) { $mday = "0" . $mday; }
	$timestamp = "$year-$mon-$mday $hour:$min:$sec";

	print "Current Time: $timestamp<br>\n";
	print "Running job.<br>";
	print "Waiting for job to complete on marburg...<br>This window will refresh every 5 seconds. Check back later for status.\n";
	print "<script>\n";
	print "setTimeout(function(){ window.location = \"status.cgi?unique=$unique\"; }, 5000);\n";
	print "</script>\n";
} else { # Job has finished.
	print "Finishing up...";
	# Get the results back to the web server.
	$var = `scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:/home/act/software/nickbild/webdata/deseq2/$unique/deseq2/deseq*.txt ./$unique/`;
	$var = `scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:/home/act/software/nickbild/webdata/deseq2/$unique/deseq2/deseq2_results.zip ./$unique/`;

	print "Download Results<br><br>\n";

	@files = glob ("./$unique/deseq*.txt");
	foreach $file (@files) {
		@temp = split (/\//, $file);
		$fileonly = $temp[-1];
		print "<a href='$file' target='_blank'>$fileonly</a><br>\n";
	}

	print "<form method='get' action='./$unique/deseq2_results.zip'><button type='submit'>Download Zip</button></form>";

	print "<a href='./$unique/settings.txt' target='_blank'>Settings File</a><br>\n";
}

exit;

