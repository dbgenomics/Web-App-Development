#!/usr/bin/perl
use CGI qw/:standard/;

print "Content-type: text/html\n\n";

# Get URL variables.
%para = ();
@tmp=("unique", "contrast", "genehide");
foreach (@tmp){
	$para{$_}=param($_);
}

$unique = $para{"unique"};
$contrast = $para{"contrast"};
$hide_gene_names = $para{"genehide"};

# Get job ID.
$var = `scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/jobs.id ./$unique/`;
open (INFILE, "./$unique/jobs.id") or die $!;
$row = <INFILE>;
@rowAry = split (/\s+/, $row);
$jobid = $rowAry[2];
close (INFILE);

# Get job status.
@status = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'qstat -f'`;
$jobstatus = "";
foreach $line (@status) {
        @lineAry = split (/\s+/, $line);
        if ($lineAry[1] eq $jobid) {
                $jobstatus = $lineAry[5];
        }
}

# Check to see if clustering job has completed.
$result = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'ls /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/run.finished'`;

if ($result eq "") {
	# Check to see if filtered file is ready.
	$var = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'ls -l /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/*.cluster.finished'`;

	# If not, display a message.
	if ($var =~ /cannot access/) {
		print "Calculating number of genes and samples...<br><br>\n";
	} else { # If so...
		# Get number of genes.
		$genes = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'wc -l /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/*.cluster'`;
		@temp = split (/\s+/, $genes);
		$genes = $temp[0];
		$genes--;

		# Get number of samples.
		$samples = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'awk -F"\t" "{print NF; exit}" /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/*.cluster'`;
		$samples--;

		# Display results, and link to cancel.
		print "Clustering $genes genes and $samples samples.<br>\n";
		print "<a href='/pl/hierarchical_clustering/form.html?name='>Cancel</a><br><br>";
	}

	# NAB 2017-05-18: Display renamed sample names.
	print "Renamed sample names:<br>";
	open (INSAMPLE, "./$unique/sample_names.txt");
	while ($samplerow = <INSAMPLE>) {
		print "$samplerow<br>";
	}
	close (INSAMPLE);
	print "<br>";

	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	$year = $year + 1900;
	$mon++;
	if ($mon < 10) { $mon = "0" . $mon; }
	if ($mday < 10) { $mday = "0" . $mday; }
	$timestamp = "$year-$mon-$mday $hour:$min:$sec";

	print "Current Time: $timestamp<br>\n";
	if ($jobstatus eq "qw") {
                print "Job queued.<br>";
        } elsif ($jobstatus eq "eqw") {
                print "Error: job status is 'eqw', an unspecified error has occurred.<br>";
        } else {
                print "Job running.<br>";
        }
	print "Waiting for job to complete on marburg...<br>This window will refresh every 10 seconds. Check back later for status.\n";
	print "<script>\n";
	print "setTimeout(function(){ window.location = \"status.cgi?unique=$unique&contrast=$contrast&genehide=$hide_gene_names\"; }, 10000);\n";
	print "</script>\n";
} else { # Clustering job has finished.
	print "Finishing up...";
	# Get the results back to the web server.
	$var = `scp -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25:/home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/* ./$unique/`;

	# Generate image of data.
	@files = glob ("./$unique/*.cdt");
	@temp = split (/\//, $files[0]);
	$files[0] = $temp[-1];


	# Increase font size with JTV file.
	$jtv = $files[0];
	$jtv =~ s/\.cdt$/.jtv/;
	open (JTV, ">./$unique/" . $jtv);
	print JTV '<DocumentConfig><UrlExtractor/><ArrayUrlExtractor/><Views><View type="Dendrogram" dock="1"><ColorExtractor><ColorSet/></ColorExtractor><ArrayDrawer/><TextView><TextView face="Dialog" size="16"><GeneSummary/></TextView><TextView face="Dialog" size="16"><GeneSummary/></TextView><TextView face="Dialog" size="16"><GeneSummary/></TextView><TextView face="Dialog" size="16"><GeneSummary included="1"/></TextView><Selection index="1"/></TextView><ArrayNameView face="Dialog" size="16"><ArraySummary included="0"/></ArrayNameView><AtrSummary included="0,3"/><GtrSummary included="0,3"/></View></Views></DocumentConfig>';
	close (JTV);

	# Determine -s value based on number of genes and samples.
	$raw = $files[0];
        $raw =~ s/\.cdt$/\.cluster/;

	$linecount = `wc -l ./$unique/$raw`;
	@temp = split (/\s+/, $linecount);
	$linecount = $temp[0];

	open (FILE, "./$unique/$raw") or die $!;
	$row = <FILE>;
	@rowAry = split (/\t/, $row);
	$numcols = scalar (@rowAry) - 1;
	close (FILE);

	if ($numcols < 12) {
		$sval1 = 600 / $numcols; # ~600 px wide.
                $sval2 = 1000 / $linecount; # ~1000 px height.
	} else {
		$sval1 = 1400 / $numcols; # ~1400 px wide.
		$sval2 = 2200 / $linecount; # ~2200 px height.
	}
	# END - Determine -s value based on number of genes and samples.

	if ($hide_gene_names eq "1") {
		$gene_names_opt = "";
	} else {
		$gene_names_opt = "-g 1";
	}

	system ("xvfb-run --auto-servernum --server-num=1 java -jar /home/yonggan/www/pl/hierarchical_clustering/TreeView-1.1.6r4-bin/TreeView.jar -r ./$unique/$files[0] -x Dendrogram -- -o ./$unique/cluster.png -s $sval1" . "x" . "$sval2 -c $contrast -a 0 $gene_names_opt -w 0 -h 100 > /dev/null");

	# Get number of filtered genes.
	$genes = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'wc -l /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/clustering/*.cluster'`;
        @temp = split (/\s+/, $genes);
        $genes = $temp[0];
        $genes--;

	$input = $raw;
	$input =~ s/\.cluster//;
	$unfiltered = `ssh -i /home/yonggan/.ssh/id_rsa_nick act\@10.1.10.25 'wc -l /home/act/software/nickbild/webdata/hierarchical_clustering/$unique/$input'`;
        @temp = split (/\s+/, $unfiltered);
        $unfiltered = $temp[0];
        $unfiltered--;

	# Get additional input from user.
	open (INFO, "./$unique/extrainfo.txt") or die "Cannot open ./$unique/extrainfo.txt," . $!;
	$criteria = <INFO>;
	$projdesc = <INFO>;
	$feature = <INFO>;
	$datatype = <INFO>;
	$log2yn = <INFO>;
	$sampcluster = <INFO>;
	$reportprefix = <INFO>;
	$criteria =~ s/\n//g;
	$projdesc =~ s/\n//g;
	$feature =~ s/\n//g;
	$datatype =~ s/\n//g;
	$log2yn =~ s/\n//g;
	$reportprefix =~ s/\n//g;
	$sampcluster =~ s/\n//g;
	$criteria =~ s/\r//g;
        $projdesc =~ s/\r//g;
        $feature =~ s/\r//g;
        $datatype =~ s/\r//g;
	$log2yn =~ s/\r//g;
	$sampcluster =~ s/\r//g;
	$reportprefix =~ s/\r//g;
	close (INFO);

	$projdescfile = $reportprefix;
	$projdescfile =~ s/\s/_/g;
	$projdescfile = substr ($projdescfile, 0, 50);
	$projdescdir = $projdescfile;
	$projdescdir = $projdescdir . "_Clustering-Data";
	system ("mkdir -p ./$unique/$projdescdir");
	system ("cp ./$unique/cluster.png ./$unique/$projdescdir/");

	# Create HTML report.
	# UPDATE 14 July 2017 KKO
	# Name the report as "_Clustering_Report.html" instead of "_report.html"
	open (HTML, ">./$unique/$projdescfile\_Clustering_Report.html") or die $!;
	print HTML "<html>\n<head>\n";
	open (INC, "./html_include.js") or die $!;
	while ($row = <INC>) {
		print HTML $row;
	}
	close (INC);
	print HTML "</head>\n<body>\n";

	# Modify text based on user input.
	$desctxt = "";
	$log2txt = "";
	if ($log2yn eq "Y") { $log2txt = "Log2-transformed ";}

	$wastransformed = "";
	if (not $log2yn eq "Y") {
		#$datatype = ucfirst($datatype); # NAB 2017-05-17: all options already have 1st letter in caps. If user enters option, it should not be modified.
		$wastransformed = "Input data was log2-transformed.";
	}

	# NAB 2016-05-25: Format gene count with thousands separator.
	$unfiltered_formatted = $unfiltered;
	$unfiltered_formatted = reverse $unfiltered_formatted;
	@temp = unpack("(A3)*", $unfiltered_formatted);
	$unfiltered_formatted = reverse join ',', @temp;

	$genes_formatted = $genes;
        $genes_formatted = reverse $genes_formatted;
        @temp = unpack("(A3)*", $genes_formatted);
        $genes_formatted = reverse join ',', @temp;

	if (not $unfiltered == $genes) {
		$desctxt = "$datatype data for $unfiltered_formatted $feature was filtered based on the $criteria, resulting in $genes_formatted rows of filtered data.";
	} else {
		$desctxt = "$datatype data for $unfiltered_formatted $feature were used for the analysis.";
	}

	$sampclusterval = "";
	if ($sampcluster eq "Y") {
		$sampclusterval = "and samples";
	}

	$feature_singular = $feature;
	$feature_singular =~ s/s$//;

	print HTML "<div style=\"margin-left:5%; max-width:75%;\">\n";
	print HTML "<h3>Hierarchical Clustering<br>\n$projdesc</h3>\n<p>$log2txt$desctxt</p>\n";
	print HTML "<p>Gene <a href='http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm'>Cluster 3.0</a> was used for hierarchical clustering.  $wastransformed  For each $feature_singular, the median across all samples was subtracted from each value.</p>\n";
	$feature_caps = ucfirst ($feature);
	print HTML "<p>$feature_caps $sampclusterval were clustered using centered correlation as the similarity measure and average linkage as the clustering method.</p>\n";
	print HTML "<p>Detailed clustering results can be viewed using the included Java Treeview application (Saldanha AJ (2004) Java Treeview - extensible visualization of microarray data. Bioinformatics 20(17), 3246-48. Available for download from <a href='http://jtreeview.sourceforge.net/'>http://jtreeview.sourceforge.net/</a>). To launch Treeview, double-click the TreeView.jar application in the Treeview folder. Using Treeview, browse to and open the $files[0] file within the $projdescdir folder. If you encounter any errors, please see the ReadMe file in the TreeView folder.</p>\n";
	print HTML "<p>Color bar in Log2 units<br><img src='$projdescdir/colorbar_contrast_$contrast.png'></p><br><img src='$projdescdir/cluster.png'>\n";
	print HTML "</div>\n</body>\n</html>\n";
	close (HTML);

	# Make data available for download.
	print "<br><br>Done!<br><br>Download Files:<br>\n";
	print "<a href='./$unique/$files[0]'>$files[0]</a><br>\n";
	$gtr = $files[0];
	$gtr =~ s/\.cdt$/\.gtr/;
	print "<a href='./$unique/$gtr'>$gtr</a><br>\n";
	$atr = $files[0];
	$atr =~ s/\.cdt$/\.atr/;
	print "<a href='./$unique/$atr'>$atr</a><br>\n";
	$jtv = $files[0];
        $jtv =~ s/\.cdt$/\.jtv/;
        print "<a href='./$unique/$jtv'>$jtv</a><br>\n";
	$raw = $files[0];
        $raw =~ s/\.cdt$/\.cluster/;
	system ("mv ./$unique/$raw ./$unique/$raw.txt");
	$raw = $raw . ".txt";
	print "<a href='./$unique/$raw'>$raw</a><br>\n";
	print "<a href='./$unique/cluster.png'>cluster.png</a><br>\n";
	print "<a href='./$unique/$projdescfile\_Clustering_Report.html'>HTML Report</a><br>\n";

	system ("mkdir -p ./$unique/Treeview; cp ./README ./$unique/Treeview/README");
	system ("cp -r ./TreeView-1.1.6r4-win/* ./$unique/Treeview");

	system ("cp ./$unique/$files[0] ./$unique/$projdescdir/");
	system ("cp ./$unique/$gtr ./$unique/$projdescdir/");
	system ("cp ./$unique/$atr ./$unique/$projdescdir/");
	system ("cp ./$unique/$jtv ./$unique/$projdescdir/");
	system ("cp ./$unique/$raw ./$unique/$projdescdir/");
	system ("cp ./colorbar_contrast_$contrast.png ./$unique/$projdescdir/");

	# Zip it up.
	system ("cd ./$unique; zip -r cluster.zip *.html $projdescdir/* Treeview/* about.txt > /dev/null");

	#print "<a href='./$unique/cluster.zip'>All Data (.zip)</a><br>\n";
	print "<form method='get' action='./$unique/cluster.zip'><button type='submit'>All Data (.zip)</button></form>";

	print "<a href='./$unique/settings.txt'>Settings File</a><br>\n";

	# Adjust contrast.
	print "<br><br>Adjust Contrast Level:";
	print "<br><a href='status.cgi?unique=$unique&contrast=1&genehide=$hide_gene_names'>Level 1</a>";
	print "<br><a href='status.cgi?unique=$unique&contrast=3&genehide=$hide_gene_names'>Level 3</a>";
	print "<br><a href='status.cgi?unique=$unique&contrast=5&genehide=$hide_gene_names'>Level 5</a>";
}

exit;

