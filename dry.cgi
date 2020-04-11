#!/usr/bin/perl
#
# Copyright (c) 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020 Thierry Banel
#
# Rsnapshot Webmin Module: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

require 'rsnapshot-lib.pl';

my @params = read_rsnapshot_config();

my $min_retain;
for $p (@params) {
    if (@$p[0] =~ m/interval|retain/) {
	$min_retain = @$p[1];
	last;
    }
}

my $rsnapshot_exe = exe();

print ui_print_header(undef, $module_info{'desc'}, undef, "overview", 1, 1);

print ui_form_start("index.cgi","GET");

print "<h2>Output of $rsnapshot_exe -t $min_retain</h2>\n";
print "<pre>\n";

open F, "$rsnapshot_exe -t $min_retain |";
while (<F>) {
    print;
}
close F;

print "</pre>\n";
print ui_form_end([[undef,"Back"]]);
