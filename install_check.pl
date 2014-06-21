#
# Copyright (c) 2012, 2013, 2014 Thierry Banel
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


do 'rsnapshot-lib.pl';

=head2 is_installed(mode)

For mode 1, returns 2 if rsnapshot is installed and configured for use by
Webmin, 1 if installed but not configured, or 0 otherwise.
For mode 0, returns 1 if installed, 0 if not

=cut
sub is_installed
{
    my ($mode) = @_;
    return $mode + 1
	if -r $config{'rsnapshot_conf'};
    return 0;
}
