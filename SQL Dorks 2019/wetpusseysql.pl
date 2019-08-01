#!/usr/bin/perl
# wetpusseysql is a MySQl pentest for vulnerbilitis of MySQL.
# Author V.Varbanovski @nu11secur1ty
#######################################
use strict;
use warnings;
use diagnostics;
use Browser::Open qw( open_browser );


print "Put here your URL...\n";
my $url = <>;
	chomp($url);
my $element = "'";
	chomp($element);
	my $action = $url.$element;
open_browser($action);
