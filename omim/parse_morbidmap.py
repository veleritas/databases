# last updated 2015-01-26 toby
import re
import sys
sys.path.append("/home/toby/global_util/")
from file_util import make_dir
from file_util import read_file

from collections import defaultdict

def parse_morbidmap():
#	returns genes[dmim] = set(gmim, gmim, gmim...) to ensure uniqueness
#	gives the list of gene mim numbers known to cause each disease mim number

	genes = defaultdict(set) # all unique gmims assosicated with dmim

	mm_loc = "/home/toby/databases/omim/data/"
	for line in read_file("morbidmap.txt", mm_loc):
		disease, gene, gmim, locus = line.split("|")
		result = re.search(r'\d{6}', disease)

#		some diseases are bad and have no disease mim identifier
		if result is not None:
			dmim = result.group()
			genes[dmim].add(gmim)

	return genes

#-------------------------------------------------------------------------------

def main():
	outloc = "/home/toby/databases/omim/data/"
	make_dir(outloc)

#	print sorted morbidmap
	genes = parse_morbidmap()
	dmims = sorted(list(genes))
	place = outloc + "sorted_morbidmap.txt"
	with open(place, "w") as out:
		for dmim in dmims:
			out.write("#" + dmim)
			for gmim in genes[dmim]:
				out.write("|" + gmim)
			out.write("\n")

	names = defaultdict(set)
	for dmim, gmims in genes.items():
		names[len(gmims)].add(dmim)

	for i, dmims in names.items():
		print "i {0} len() {1}".format(i, len(dmims))

if __name__ == "__main__":
	main()
