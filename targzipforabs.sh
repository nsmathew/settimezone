#!/usr/bin/bash
#script to tar and gzip source files for enabling building using ABS
#The pkg name and version are read from the PKGBUILD file directly
#Should be run from the parent diretcory of the project(assuming PKGBUILD is also in same location)
#Copyright Nitin Mathew 2013 <nitn_mathew2000@hotmail.com>

VER=`grep pkgver PKGBUILD | head -n1 | sed 's/ *$//g' | awk -F '=' '{print $2}'`
PKG=`grep pkgname PKGBUILD | head -n1 | sed 's/ *$//g' | awk -F '=' '{print $2}'`
mkdir -p archive
tar --exclude "./archive" --exclude "./.git" --exclude "./nbproject" --exclude $0 -cvf ./archive/${PKG}_v${VER}.tar .
gzip ./archive/$PKG_v$VER.tar
ls -lrt ./archive
