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

print ui_print_header(undef, $module_info{'desc'}, undef, "overview", 1, 1);

print ui_form_start("saveanacron.cgi","POST");

my @params = read_rsnapshot_config();

my $rsnapshot_exe = exe();

# --------------------------------------

print <<EOF;
<h2>Anacron configuration</h2>

<ul>
<li><b>Anacron</b> is recommended for computers that are turned on and off repeatedly.

<li><b><a href="cron.cgi">Cron</a></b> is recommended for computers always on,
or snapshots happening more often than daily.

<li>Webmin does not yet support Anacron.
<br>In the meantime, this page offers manual <b>text editing</b>
for the configuration file.

<li>The suggested lines should be <b>added to the $anacrontab file</b>
(unless they are already there).
<br>Change numerical values to fit your needs.
<br><b>Do not forget</b> to replace question marks with numerical values.

<li>Job description lines are of this form:
<ul>
<li><code><b>period delay identifier command</b></code>
<li>The <b>period</b> is specified in days since the command was last executed.
<br>It may also be the special word <code><b>\@month</b></code> to ensure the job is run once a month.
<li>The <b>delay</b> is the number of minutes to wait before actually running the command.
<li>Fields are separated by blank spaces or tabs.
</ul>
<li>Anacron cannot run commands <b>more often than daily</b>.
<br>Therefore if you want high frequency snapshots (for instance hourly)
then you'd better use <a href="cron.cgi">Cron</a>.

<li>Be sure to run high frequency snapshots <b>after low frequency</b> ones.
<br>For instance, daily snapshots should be run a few minutes afrer weekly ones.

</ul>
EOF
#'
# --------------------------------------

my $nbcols = 2;
my $nblines = 0;

my $config = read_anacron_config();
my $configtabs = $config;  # untabify (thanks Stas Bekman)
$configtabs =~ s/\t/' ' x (8 - length($`) % 8)/eg;

while ($configtabs =~ m/(^.*\n)/mg)
{
    $nbcols = length $1
	if $nbcols < length $1;
    $nblines++;
}

my $txt = "# days    minutes id                   command\n";
my $nblinestoadd = 1;
for $p (@params) {
    next unless $p->[0] eq 'retain';
    $interv = $p->[1];
    my $p = sprintf "rsnapshot_%-10s %s %-s", $interv, $rsnapshot_exe, $interv;
    my $t;
    if    ($interv =~ m/hour/i)   { $t = "# not possible    $p\n"; }
    elsif ($interv =~ m/da[iy]/i) { $t = "1         95      $p\n"; }
    elsif ($interv =~ m/week/i)   { $t = "7         93      $p\n"; }
    elsif ($interv =~ m/month/i)  { $t = "\@monthly  91      $p\n"; }
    elsif ($interv =~ m/year/i)   { $t = "365       89      $p\n"; }
    else                          { $t = "?         ?       $p\n"; }
    $nblinestoadd++;
    $txt .= $t;
    $nbcols = length $t
	if $nbcols < length $t;
}

# -------------------------------------

print &ui_table_start($anacrontab,undef,1);
print &ui_table_row ("",
		     ui_textarea ("thefile",
				  $config,
				  $nblines+$nblinestoadd,
				  $nbcols,
				  "off",
				  undef,
				  'spellcheck="false"'));
print &ui_table_end;

# --------------------------------------

print "<p>\n";

print &ui_table_start("Suggested lines to add",undef,1);
print &ui_table_row ("",
		     ui_textarea ("toadd",
				  $txt,
				  $nblinestoadd,
				  $nbcols,
				  "off",
				  undef,
				  'spellcheck="false" readonly="true"'));
print &ui_table_end;

print <<EOF;
<script>
function copy()
{
    var toadd   = window.document.getElementsByName("toadd")[0];
    var thefile = window.document.getElementsByName("thefile")[0];
    thefile.value += toadd.value;
    toadd.value = "";
}
</script>
<input type="button" onclick="javascript:copy();" value="Copy-Paste" />
<a href="../man/view_man.cgi?page=anacron">[View Anacron Man Page]</a>
<a href="../man/view_man.cgi?page=anacrontab&sec=5">[View Anacrontab Man Page]</a>

EOF

# --------------------------------------

print ui_form_end([["index","Configure"],["save","Save"],["anacron","Refresh"],["cron","prefer Cron"]]);

print ui_print_footer('/', $text{'index'});
