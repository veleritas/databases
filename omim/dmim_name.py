# last updated 2015-03-03 toby
"""
Reads and returns the names of OMIM diseases.
"""
import os
HOME = os.path.expanduser("~")
import sys
sys.path.append(os.path.join(HOME, "global_util"))
from file_util import read_file

def read_omim_names():
	dmim_name = dict()
	inloc = os.path.join(HOME, "databases/omim/data")
	for line in read_file("dmim_name.txt", inloc):
		dmim, name = line.split('|')
		dmim_name[dmim] = name

	return dmim_name
