#!/usr/bin/perl
#
# Copyright (c) 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022 Thierry Banel
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

print ui_print_header(undef, $module_info{'desc'}, undef, "overview", 1, 1);

print ui_form_start("cronforwd.cgi","GET");

my @params = read_rsnapshot_config();

my $rsnapshot_exe = exe();

# --------------------------------------

foreign_require("cron","cron-lib.pl");

my @cols = qw( user command active mins hours days months weekdays index active );
my @crons = cron::list_cron_jobs();

#print "<table>\n";
#print "<tr>\n";
#for $c (@cols) { print "<td><b>$c</b></td>\n" }
#print "</tr>\n";
#for $c (@crons) {
#    print "<tr>";
#    for $k (@cols) {
#        printf "<td>%s</td>\n", $c->{$k};
#    }
#    print "</tr>\n";
#}
#print "</table>\n";

sub find_matching_job
{
    my ($interval) = @_;
    for $c (@crons) {
	next unless $c->{command} =~ m/rsnapshot/;
	next unless $c->{command} =~ m/$interval/;
	return $c;
    }
    return undef;
}


# --------------------------------------

print <<EOF;
<h2>Cron configuration</h2>

<ul>
<li><b>Cron</b> is recommended for computers always on,
or snapshots happening more often than daily.

<li><b><a href="anacron.cgi">Anacron</a></b> is recommended for computers that are turned on and off repeatedly.

<li>For missing jobs, values are only suggestions. Change them to fit your needs.

<li>Be sure to run high frequency snapshots <b>after low frequency</b> ones.
<br>For instance, daily snapshots should be run a few minutes afrer weekly ones.

</ul>
EOF

# --------------------------------------

print ui_columns_start(
[
"Active",
"Min",
"Hour",
"DoM",
"Month",
"DoW",
"Command / Actual command",
"Job"
]);


for $p (@params) {
    next unless $p->[0] eq 'retain';
    $interv = $p->[1];
    
    my $actualcomm = "(missing)";
    my $job = find_matching_job($interv);
    if (defined $job) {
	@p = ($job->{active} ? "active" : "disabled",
	      $job->{mins},
	      $job->{hours},
	      $job->{days},
	      $job->{months},
	      $job->{weekdays});
	$actualcomm = $job->{command};
    } else {
	if    ($interv =~ m/hour/i)   { @p = ("missing", "47", "7,15,23", "* ", "* ", "* "); }
	elsif ($interv =~ m/da[iy]/i) { @p = ("missing", "35", "23",      "* ", "* ", "* "); }
	elsif ($interv =~ m/week/i)   { @p = ("missing", "29", "23",      "* ", "* ", "5 "); }
	elsif ($interv =~ m/month/i)  { @p = ("missing", "25", "23",      "9 ", "* ", "* "); }
	elsif ($interv =~ m/year/i)   { @p = ("missing", "17", "23",      "31", "12", "* "); }
	else                          { @p = ("missing", ""  , ""  ,      ""  , ""  , ""  ); }
    }
    my $j
    = defined($job)
    ? sprintf "<a href='../cron/edit_cron.cgi?idx=%s'>Edit</a>", $job->{index}
    :         "<a href='../cron/edit_cron.cgi?new=1' >Create</a>";
    print ui_columns_row([$p[0],$p[1],$p[2],$p[3],$p[4],$p[5],
			  sprintf("%s %s<br>%s", $rsnapshot_exe, $interv, $actualcomm),
			  $j]);
}

print ui_table_end();

# --------------------------------------

print <<EOF;
<p>
<a href="../cron/index.cgi">[Go to Cron manager]</a>
<a href="../cron/edit_cron.cgi?new=1">[Create a new Cron job]</a>
<a href="../man/view_man.cgi?page=cron">[View Cron Man Page]</a>
<a href="../man/view_man.cgi?page=crontab&sec=5">[View Crontab Man Page]</a>
<p>
EOF

print ui_form_end([["index","Configure"],["refresh","Refresh"],["anacron","prefer Anacron"]]);
