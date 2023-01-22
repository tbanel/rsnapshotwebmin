#!/usr/bin/perl
#
# Copyright (c) 2012-2023 Thierry Banel
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

sub number_box
{
    my ($name,$i) = @_;
    my @interv = ("", $i!=0..2*$i+24);
    ui_select ($name, $i, \@interv, 1, 0, 1);
}

sub multi_col
{
    my $head = shift;
    ui_table_row ($head, join "</td><td>", @_);
}

# --------------------------------------

print ui_print_header(undef, $module_info{'desc'}, undef, "overview", 1, 1);

my @params = read_rsnapshot_config();

# add empty additional fields
# they will be ignore when saving if still empty
for my $i (1..2) {
    unshift @params, ["backup","","./",""];
    unshift @params, ["ixclude",""];
    unshift @params, ["retain","",""];
}

# add empty additional fields
# they will be ignore when saving if still empty
for my $i (1..3) {
    push @params, ["backup","","./",""];
    push @params, ["ixclude",""];
    push @params, ["retain","",""];
}

for $p (@params) {
    $params{@$p[0]} = $p;
}

# --------------------------------------

print ui_form_start("save.cgi","POST");

@tabs = ( [ 'directories', 'Directories' ],
	  [ 'ixclude'    , 'Excludes' ],
	  [ 'intervals'  , 'Retentions' ],
          [ 'log'        , 'Log' ],
          [ 'advanced'   , 'Advanced options' ] );

print ui_tabs_start(\@tabs, 'mode', 'directories',1);
print ui_tabs_start_tab('mode', 'directories');

# --------------------------------------

print ui_table_start("Destination directory",undef,1);
print multi_col ("",
		 hlink("<b>Root of backup directory<br>(absolute path)</b>","root"));
print multi_col ("",
		 ui_filebox("snapshot_root",$params{snapshot_root}->[1],30));
print multi_col ("",
		 hlink("<b>Do not create root</b>","root"),
		 ui_checkbox("no_create_root","1",undef,$params{no_create_root}->[1]));
print ui_table_end();

# --------------------------------------

$backupo = "backupo00";
$backupd = "backupd00";
$backupp = "backupp00";

print "<p/>";
print ui_table_start("Directories to backup",undef,1);
print multi_col ("",
		 hlink("<b>Origin<br>(absolute path)</b>"          ,"backup"),
		 hlink("<b>Destination<br>(relative to root)</b>"  ,"backup"),
		 hlink("<b>Additional parameters<br>(optional)</b>","backup"));
print multi_col ("","<hr/>","<hr/>","<hr/>");
for $p (@params) {
    if (@$p[0] eq "backup") {
	print multi_col ("",
			 ui_filebox($backupo++,@$p[1],30),
			 ui_textbox($backupd++,@$p[2],20),
			 ui_textbox($backupp++,@$p[3],20));
    }
}
print ui_table_end();

print ui_tabs_end_tab('mode', 'directories');

# --------------------------------------

print ui_tabs_start_tab('mode', 'ixclude');

print ui_table_start("Includes, Excludes","name='bbb'",1);
print multi_col ("",
		 hlink("<b>To include<br>or to exclude</b>","inexclude"),
		 hlink("<b>Pattern, absolute or relative<br>(* = anything)</b>","inexclude"));
print multi_col ("","<hr/>","<hr/>");

@options = (["include","include"],["exclude","exclude"]);
$exincludef = "exincludef00";
$exincluded = "exincluded00";
my $nb = 0;
for $p (@params) {
    if (@$p[0] =~ m/^include|exclude|ixclude$/) {
	print multi_col ("",
			 ui_radio  ($exincludef++,@$p[0],\@options),
			 ui_textbox($exincluded++,@$p[1],40),
			# ui_up_down_arrows("javascript:upline($nb);", "downline", 1, 1)
	    );
	$nb++;
    }
}
print ui_table_end();

print ui_tabs_end_tab('mode', 'ixclude');

# --------------------------------------

print ui_tabs_start_tab('mode', 'intervals');

print ui_table_start("Retained intervals",undef,1);
print multi_col ("",
		 hlink("<b>Label<br>(any word)</b>"       ,"retain"),
		 hlink("<b>Number of<br>occurences</b>"   ,"retain"));
print multi_col ("","<hr/>","<hr/>","<hr/>");
$retaint = "retaint00";
$retainn = "retainn00";
for $p (@params) {
    if (@$p[0] =~ m/interval|retain/) {
	print multi_col ("",
	    ui_textbox($retaint++,@$p[1],12),
	    number_box($retainn++,@$p[2]));
    }
}
print ui_table_end();

# --------------------------------------

print ui_tabs_end_tab('mode', 'intervals');

# --------------------------------------

print ui_tabs_start_tab('mode', 'log');

print ui_table_start("Logs",undef,1);
{
    my @interv = ( [1,"Quiet (fatal errors only)"],
		   [2,"Default (warnings and errors)"],
		   [3,"Verbose (show shell commands)"],
		   [4,"Extra verbose (more detail)"],
		   [5,"Debug (all information)"]);
    print ui_table_row(hlink("verbose","verbose"),
		       ui_select("verbose",$params{verbose}->[1],
				 \@interv,
				 1, 0, 1));
    print ui_table_row(hlink("loglevel","verbose"),
		       ui_select("loglevel",$params{loglevel}->[1],
				 \@interv,
				 1, 0, 1));
    print ui_table_row(hlink("logfile","verbose"),
		       ui_filebox("logfile",$params{logfile}->[1],40));
    print ui_table_row(hlink("lockfile","lockfile"),
		       ui_filebox("lockfile",$params{lockfile}->[1],40));
print multi_col(hlink("stop on stale lockfile","lockfile"),
		ui_checkbox("stop_on_stale_lockfile", "1", undef, $params{stop_on_stale_lockfile}->[1]));

}
print ui_table_end();

print ui_tabs_end_tab('mode', 'log');

# --------------------------------------

print ui_tabs_start_tab('mode', 'advanced');

print ui_table_start("Switches",undef,1);
print multi_col (hlink("config file version ","config_version"),
		 ui_textbox("config_version",
			    $params{config_version}->[1]||"",
			    20));
print multi_col(hlink("one file system","one_fs"),
		ui_checkbox("one_fs","1", undef, $params{one_fs}->[1]));
print multi_col(hlink("sync first","sync_first"),
		ui_checkbox("sync_first","1", undef, $params{sync_first}->[1]));
print multi_col(hlink("use lazy deletes","use_lazy_deletes"),
		ui_checkbox("use_lazy_deletes","1", undef, $params{use_lazy_deletes}->[1]));
print multi_col (hlink("command rsync","rsync"), ui_filebox("cmd_rsync",$params{cmd_rsync}->[1],20));
print multi_col(hlink("rsync number of tries","rsync"),
		number_box("rsync_numtries",$params{rsync_numtries}->[1])||"0");
print multi_col (hlink("rsync short args","rsync"),
		 ui_textbox("rsync_short_args",
			    $params{rsync_short_args}->[1]||"",
			    20));
print multi_col (hlink("rsync long args","rsync"),
		 ui_textbox("rsync_long_args",
			    $params{rsync_long_args}->[1]||"",
			    20));
print multi_col(hlink("rsync link destination","rsync"),
		ui_checkbox("link_dest","1", undef, $params{link_dest}->[1]));
print multi_col (hlink("command ssh","ssh"), ui_filebox("cmd_ssh",$params{cmd_ssh}->[1],20));
print multi_col (hlink("ssh args","ssh"),
		 ui_textbox("ssh_args",
			    $params{ssh_args}->[1]||"",
			    20));
print multi_col (hlink("command copy","cmd"), ui_filebox("cmd_cp",$params{cmd_cp}->[1],20));
print multi_col (hlink("command remove","cmd"), ui_filebox("cmd_rm",$params{cmd_rm}->[1],20));
print multi_col (hlink("command logger","cmd"), ui_filebox("cmd_logger",$params{cmd_logger}->[1],20));
print multi_col (hlink("command rsnapshot diff","cmd"), ui_filebox("cmd_rsnapshot_diff",$params{cmd_rsnapshot_diff}->[1],20));
print multi_col (hlink("command pre-exec","cmd"), ui_filebox("cmd_preexec",$params{cmd_preexec}->[1],20));
print multi_col (hlink("command post-exec","cmd"), ui_filebox("cmd_postexec",$params{cmd_postexec}->[1],20));
print multi_col (hlink("command disk usage","du"), ui_filebox("cmd_du",$params{cmd_du}->[1],20));
print multi_col (hlink("du args","du"),
		 ui_textbox("du_args",
			    $params{du_args}->[1]||"",
			    20));
print ui_table_end();

print ui_tabs_end_tab('mode', 'advanced');

# --------------------------------------

print ui_tabs_end(1);

print ui_form_end([[undef,"Save"],["index","Reset"],["dry","Dry Run"],["cron","Cron"],["anacron","Anacron"]]);

print ui_print_footer('/', $text{'index'});
