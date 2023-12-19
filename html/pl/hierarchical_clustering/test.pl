#!/usr/bin/perl

$a = 25100;
$a = reverse $a;
@temp = unpack("(A3)*", $a);
$a = reverse join ',', @temp;
print $a . "\n";

