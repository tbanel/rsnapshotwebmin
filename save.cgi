#!/usr/bin/perl
#
# Copyright (c) 2012 Thierry Banel
#
# Rsnapshot Webmin Module: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Save the rsnapshot configuration
# The input is given in the %in variable
# The output is the Rsnapshot config file (usualy /etc/rsnapshot.conf )

require 'rsnapshot-lib.pl';
require 'web-lib-funcs.pl';

ReadParse(); # fills %in, @in, $in

if (defined $in{index}) { redirect('index.cgi' ); }
else {

    my @newsettings;

    for $k (@simpleflags) {
	push @newsettings, sprintf "%s\t%s\n", $k, $in{$k}
	if $in{$k};
    }

    for (my $o="backupo00"; ; $o++) {
	last unless exists $in{$o};
	next unless $in{$o};
	my $d = $o; $d =~ s/backupo/backupd/;
	my $p = $o; $p =~ s/backupo/backupp/;
	push @newsettings, sprintf "backup\t%s\t%s\t%s\n", $in{$o}, $in{$d}, $in{$p};
    }

    for (my $d="exincluded00"; ; $d++) {
	last unless exists $in{$d};
	next unless $in{$d};
	my $f = $d; $f =~ s/exincluded/exincludef/;
	next unless $in{$f};
	push @newsettings, sprintf "%s\t%s\n", $in{$f}, $in{$d};
    }

    for (my $t="retaint00"; ; $t++) {
	last unless exists $in{$t};
	next unless $in{$t};
	my $n = $t; $n =~ s/retaint/retainn/;
	push @newsettings, sprintf "retain\t%s\t%s\n", $in{$t}, $in{$n};
    }

    merge_rsnapshot_config(@newsettings);

    if    (defined $in{dry}    ) { redirect('dry.cgi' ); }
    elsif (defined $in{cron}   ) { redirect('cron.cgi'); }
    elsif (defined $in{anacron}) { redirect('anacron.cgi'); }
    else                         { redirect(''); }
}
