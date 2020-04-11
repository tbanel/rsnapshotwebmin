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
require 'web-lib-funcs.pl';

ReadParse(); # fills %in, @in, $in

if    (defined $in{index}  ) { redirect('index.cgi' ); }
elsif (defined $in{cronmng}) { redirect('../cron/index.cgi'); }
elsif (defined $in{refresh}) { redirect('cron.cgi'); }
elsif (defined $in{anacron}) { redirect('anacron.cgi'); }
else                         { redirect(''); }
