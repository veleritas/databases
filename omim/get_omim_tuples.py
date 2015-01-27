# last updated 2015-01-27 toby

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

def load_converted_morbidmap():
	dmim_cuis = dict()
	gene_ids = dict()

	inloc = "/home/toby/databases/omim/data"
	cur_dmim = ""
	for i, line in enumerate(read_file("converted_morbidmap.txt", inloc)):
		line = line.lstrip('\t')

		vals = line.split('|')
		if i % 2 == 0: # dmim
			if len(vals) == 1: # no cuis
				cur_dmim = ""
			else:
				cur_dmim = vals[0]
				dmim_cuis[cur_dmim] = set(vals[1:])
		elif cur_dmim:
			gene_ids[cur_dmim] = set(vals)

	return (dmim_cuis, gene_ids)

def get_omim_tuples():
#	returns a set of unique (geneID, CUI) tuples
#	derived from omim morbidmap, and converted
#	using entrez eutils

	dmim_cuis, gene_ids = load_converted_morbidmap()

	omim_tuples = set()
	for dmim, cuis in dmim_cuis.items():
		omim_tuples |= set([(geneID, cui) for cui in cuis for geneID in gene_ids[dmim]])

	return omim_tuples
