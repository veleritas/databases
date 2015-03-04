# last updated 2015-03-03 toby
"""
Extracts the gene-disease relationships from OMIM's morbidmap
as a set of (gmim, dmim) pairs. Also returns the name of each
disease mim identifier (dmim, gmim = gene mim) for easy
reference.
"""
import os
HOME = os.path.expanduser("~")

import re
import sys
sys.path.append(os.path.join(HOME, "global_util"))
from file_util import make_dir
from file_util import read_file

from collections import defaultdict

def info(s):
	"""
	Gives the name and identifier of a particular OMIM disease.
	"""
	result = re.search(r'\d{6}', s)
	if result is not None:
		dmim = result.group()
		name = s.rsplit(",", 1)[0]
		return (dmim, name)

	return ()

def parse_morbidmap():
	"""
	Returns the set of unique genes associated with a particular
	OMIM disease in the format:
		genes[dmim] = set(gmim, gmim, gmim...)
	"""
	genes = defaultdict(set) # all unique gmims assosicated with dmim
	name = dict() # name of dmim
	loc = os.path.join(HOME, "databases/omim/data")
	for line in read_file("morbidmap.txt", loc):
		disease, gene, gmim, locus = line.split("|")

		res = info(disease)
		if res:
			genes[res[0]].add(gmim)
			name[res[0]] = res[1]

	with open(os.path.join(loc, "dmim_name.txt"), "w") as out:
		for dmim, disease_name in name.items():
			out.write("{0}|{1}\n".format(dmim, disease_name))

	return genes

#-------------------------------------------------------------------------------

def main():
	make_dir("./data/")

#	print sorted morbidmap
	genes = parse_morbidmap()
	with open("./data/sorted_morbidmap.txt", "w") as out:
		for dmim, gmims in sorted(genes.items()):
			out.write("#{0}|{1}\n".format(dmim, "|".join(gmims)))

#	determine the distribution of # of genes per disease
	names = defaultdict(set)
	for dmim, gmims in genes.items():
		names[len(gmims)].add(dmim)

	for i, dmims in names.items():
		print "i {0} len() {1}".format(i, len(dmims))

if __name__ == "__main__":
	main()
