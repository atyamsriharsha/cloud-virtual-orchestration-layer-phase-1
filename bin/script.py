#!/usr/bin/env python
sudo apt-get install flask
sudo apt-get install libvirt
import os
import sys
import libvirt
from flask import Flask
from random import randomint
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script pm_file image_file vm_type"
		exit(1)
	os.chdir("../src")
	os.system("python start.py " + sys.argv[1] + " " +sys.argv[2] + " " +sys.argv[3])

