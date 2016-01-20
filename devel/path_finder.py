#!/usr/bin/env python

import os

bindir =  os.path.dirname(os.path.abspath(__file__))
basedir = os.path.dirname(bindir)
ext_basedir = os.path.join(os.path.dirname(basedir),'tsctl2')

print "bindir=" , bindir
print "basedir=" , basedir
print "ext_basedir=" , ext_basedir

