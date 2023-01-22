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

=head1 rsnapshot-lib.pl

Functions for rsnapshot

=cut

use WebminCore;
init_config();

=head2 read_rsnapshot_config()

Reads the RSnapshot config file (usually /etc/rsnapshot.conf)
Returns an array of non-comment lines as pairs key-value

=cut

sub read_rsnapshot_config
{
    my @result;
    open(CONF, $config{'rsnapshot_conf'});
    while (<CONF>) {
	chomp;
	next if m/^#/;
	next if m/^\s*$/;
	my @s = split /\t+/;
	push @result, \@s;
    }
    close CONF;
    return @result;
}

=head2 read_rsnapshot_config()

Reads the RSnapshot config file (usually /etc/rsnapshot.conf)
Returns an array of lines, including comments and blank lines

=cut

sub read_rsnapshot_config_raw
{
    my @result;
    open(CONF, $config{'rsnapshot_conf'});
    while (<CONF>) {
	push @result, $_;
    }
    close CONF;
    return @result;
}

=head2 write_rsnapshot_config()

Write the RSnapshot config file (usually /etc/rsnapshot.conf)

=cut

sub write_rsnapshot_config
{
    open CONF, ">$config{'rsnapshot_conf'}";
    for my $pair (@_) {
	printf "%s\n", join "\t", $pair;
    }
    close CONF;
}

=head2 @simpleflags, %simpleflags

The list of Rsnapshot simple flags
(non-simple flags are 'backup', 'exclude', 'include', 'retain')

=cut

@simpleflags =
    qw(
 verbose
 loglevel
 rsync_numtries
 rsync_short_args
 rsync_long_args
 lockfile
 logfile
 snapshot_root
 no_create_root
 du_args
 ssh_args
 one_fs
 link_dest
 sync_first
 use_lazy_deletes
 stop_on_stale_lockfile
);

for my $f (@simpleflags) {
    $simpleflags{$f} = 1;
}

# transfers settings matching regexp
# from  @newsettings  to the end of  @newraw

my @newsettings;
my @newraw;

sub transfer
{
    my ($regex) = @_;
    for (my $i=0; $i<=$#newsettings; $i++) {
	if ($newsettings[$i] =~ m/$regex/) {
	    push @newraw, $newsettings[$i];
	    splice @newsettings, $i, 1;
	    return 1;
	}
    }
    return undef;
}

=head2 merge_rsnapshot_config

Merges the config file with settings passed as parameters
One parameter is a line which must appear as-is in the config file
An attempt is made to keep the new config file as close as possible to the old
by keeping comments
and by putting the new options at the same location as the old ones

=cut

sub merge_rsnapshot_config
{
    @newsettings = @_;
    @newraw = ();

    for my $p (read_rsnapshot_config_raw()) {
	if ($p =~ m/\s*#/) {
	    push @newraw, $p;
	} elsif ($p =~ m/^\s*$/) {
	    push @newraw, $p;
	} elsif ($p =~ m/^(retain|interval)\W/) {
	    transfer("^retain\W");
	} elsif ($p =~ m/^(include|exclude)\W/) {
	    transfer("^(include|exclude)\W");
	} elsif ($p =~ m/^backup\W/) {
	    transfer("^backup\W");
	} elsif ($p =~ m/^(\w+)/) {
	    my $flag = $1;
	    if (!transfer("^$flag\\W") && !exists $simpleflags{$flag}) {
		push @newraw, $p;
	    }
	} else {
	    push @newraw, $p;
	}
    }
    
    push @newraw, @newsettings;

    open_tempfile(F, ">/tmp/l");
    for my $p (@newraw) {
	print_tempfile(F,"$p");
    }
    close_tempfile(F);
    
    lock_file($config{'rsnapshot_conf'});
    copy_source_dest("/tmp/l",$config{'rsnapshot_conf'});
    # Log the change
    unlock_file($config{'rsnapshot_conf'});
}

=head2 anacrontab

A variable to hold the Anacron configuration file
Usually it is /etc/anacrontab

=cut

$anacrontab = "/etc/anacrontab";

=head2 read_anacron_config

Reads and returns the contents of /etc/anacrontab file

=cut

sub read_anacron_config
{
    open (F, $anacrontab);
    my $text;
    while (<F>) { $text .= $_; }
    close F;
    return $text;
}

=head2 replace_anacron_config

Replaces the file /etc/anacrontab with the given text

=cut

sub replace_anacron_config
{
    my ($text) = @_;
    return if $text eq read_anacron_config();
    open_tempfile(F, ">/tmp/l");
    print_tempfile(F,$text);
    close_tempfile(F);
    lock_file($anacrontab);
    copy_source_dest("/tmp/l",$anacrontab);
    # Log the change
    unlock_file($anacrontab);
}

=head2 exe

Return the Rsnapshot executable.
If a non-standard configuration file is in use, it is returned as well,
for instance:
  rsnapshot -c /etc/rsnapshot-alt.conf

=cut

sub exe
{
    my $conf = $config{'rsnapshot_conf'};
    my $x = "/usr/bin/rsnapshot";
    $x = "$x -c $conf"
	unless $conf eq "/etc/rsnapshot.conf";
    return $x;
}

1;
