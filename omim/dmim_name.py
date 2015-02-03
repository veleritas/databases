# last updated 2015-02-02 toby
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

def read_omim_names():
	dmim_name = dict()
	inloc = "/home/toby/databases/omim/data/"
	for line in read_file("dmim_name.txt", inloc):
		dmim, name = line.split('|')
		dmim_name[dmim] = name

	return dmim_name
