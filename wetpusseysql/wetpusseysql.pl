#!/usr/bin/perl
#
# wetpusseysql is a program for testing of MySQL vulnerabilities.
# This is a simple and strong program for testing of vulnerabilities of MySQL server
# Author V.Varbanovski @nu11secur1ty
####################################################################################
use strict;
use warnings;
use diagnostics;
use Browser::Open qw( open_browser );
use Term::ANSIColor;


print color('bold blue');

print"                           o8                                                                                               o888 
oooo  o  oooo ooooooooo8 o888oo ooooooooo  oooo  oooo   oooooooo8  oooooooo8   ooooooooo8 oooo   oooo oooooooo8    ooooooooo 888 
 888 888 888 888oooooo8   888    888    888 888   888  888ooooooo 888ooooooo  888oooooo8   888   888 888ooooooo  888    888  888 
  888888888  888          888    888    888 888   888          888        888 888           888 888          888 888    888  888 
   88   88     88oooo888   888o  888ooo88    888o88 8o 88oooooo88 88oooooo88    88oooo888     8888   88oooooo88    88ooo888 o888o
                                o888                                                       o8o888                       888o \n\n\n";
print color('reset');

print color('bold red');
print "Use Ctrl + C to stop the wetpusseysql\n";
	print color('reset');

print "Please put your correct URL here\n";
print "which you will copy from your browser.\n";

my $url = <>;
	chomp($url);
my $element_vulnerability_prostak = "'";
	chomp($element_vulnerability_prostak);
	my $action = $url.$element_vulnerability_prostak;
open_browser($action);
exit;
