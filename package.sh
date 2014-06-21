#!/bin/sh
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

TEMP="/tmp"
PACK="rsnapshot"
# Beware! do not use a version number like that:
#   PACK="rsnapshot-0.3"
# otherwise there are plenty of problems with parallel versions
# of the module within Webmin

mkdir $TEMP/$PACK

rsync -pEtrvu \
    --delete \
    --delete-excluded \
    --include '*.cgi' \
    --include '*.info' \
    --include '*.pl' \
    --include '*.gif' \
    --include '*.html' \
    --include '*.gif' \
    --include '*.sh' \
    --include 'CHANGELOG' \
    --include 'lang/en' \
    --exclude='.git' \
    --exclude='*~' \
    --exclude TAGS \
    ./ $TEMP/$PACK

chdir $TEMP
tar cvfz $PACK.wbm.gz $PACK
