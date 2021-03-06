# coding: utf-8
# For Python < 2.6
from __future__ import with_statement

import os

from ubik_toolbelt.logger import stream_logger

def create(package_name):
	name = package_name

	control_skel = """#!/bin/bash

NAME="%s"
VERSION=0.1
RELEASE=0
DESCRIPTION=""
REQUIRES=""

function pre_install(){
    echo "Pre-install $NAME $VERSION-$RELEASE ..."
}

function post_install(){
    echo "Post-install $NAME $VERSION-$RELEASE ..."
}

function pre_remove(){
    echo "Pre-remove $NAME $VERSION-$RELEASE ..."
}

function post_remove(){
    echo "Post-remove $NAME $VERSION-$RELEASE ..."
}

function pre_update(){
    echo "Pre-update $NAME $VERSION-$RELEASE ..."
}

function post_update(){
    echo "Post-update $NAME $VERSION-$RELEASE ..."
}

function purge(){
    echo "Purge $NAME $VERSION-$RELEASE ..."
}""" % name

	make_sh_skel = """#!/bin/bash

#################################
# Variables
#################################
SRC="$(pwd)/src"
DST="$(pwd)/build"
#################################

#################################
# Install
#################################
function install(){
	# Here your install procedure
	# Never forget to user $SRC and $DST
	true
}
#################################

if [ -z "$(ls -a | grep .libs.sh)" ]; then
	echo "Need to be in package root"
	exit 1
else
	. .libs.sh
fi"""

	libs_sh_skel = """#!/bin/bash

#
# This file contains libs to create package archive
# Be carefull
#

function files_listing(){
	cd build
	find ./ -type f > ../$NAME/files.lst
	find ./ -type l >> ../$NAME/files.lst
	cd ..
}

function files_blacklist(){
	for line in $(cat ./blacklist); do
		cat ./$NAME/files.lst | grep -v "$line" > ./$NAME/files.lst.tmp
		mv ./$NAME/files.lst.tmp ./$NAME/files.lst
	done
	rm ./$NAMEfiles.lst.tmp > /dev/null 2>&1
}

function help(){
	echo "Usage: make.sh (install|package|purge)"
	echo ""
	echo "  install     Build package"
	echo "  package     Create package archive"
	echo "  clean       Clean old archives"
	echo ""
}

#################################
# Make Package
#################################
function package(){
	touch ./control
	chmod +x ./control
	mkdir $NAME

	files_listing
	files_blacklist

	cd build
	tar cfj ../$NAME/files.bz2 -T ../$NAME/files.lst
	cd ..
	cp ./control $NAME
	cp ./blacklist $NAME
	tar cf $NAME.tar $NAME 
}
#################################

#################################
# Clean
#################################
function clean(){
	rm -rf $NAME > /dev/null 2>&1
	rm $NAME.tar > /dev/null 2>&1
	rm files.bz2 > /dev/null 2>&1
	rm files.lst > /dev/null 2>&1
}
#################################

. control
if [ "$1" == "install" ]; then
	install
elif [ "$1" == "package" ]; then
	package
elif [ "$1" == "clean" ]; then
	clean
else
	help
fi"""

	stream_logger.info(' :: Create %s package structure' % name)
	os.makedirs(name)
	os.chdir(name)
	os.makedirs('build')
	os.makedirs('src')
	open('blacklist', 'w').close()
	with open('control', 'w') as control:
		control.write(control_skel)
	with open('make.sh', 'w') as make_sh:
		make_sh.write(make_sh_skel)
	with open('.libs.sh', 'w') as libs_sh:
		libs_sh.write(libs_sh_skel)
	os.chmod('control', 0755)
	os.chmod('make.sh', 0755)
	stream_logger.info(' :: Done')
