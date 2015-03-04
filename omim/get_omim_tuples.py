# last updated 2015-03-03 toby
"""
Returns all of the OMIM gene-disease relationships in
Entrez gene ID, UMLS CUI format.
"""
import os
HOME = os.path.expanduser("~")
import sys
sys.path.append(os.path.join(HOME, "global_util"))
from file_util import read_file

def load_converted_morbidmap():
	"""
	For the genes and diseases in OMIM morbidmap, returns
	the Entrez gene IDs and the UMLS CUIs that the information
	corresponds to.
	"""
	dmim_cuis = dict()
	gene_ids = dict()
	inloc = os.path.join(HOME, "databases/omim/data")
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
	"""
	Returns all unique (Entrez gene ID, UMLS CUI) pairs
	derived from OMIM morbidmap. Note that this inflates
	the total number of gene-disease pairs because OMIM
	disease identifiers map to many UMLS CUIs.
	"""
	dmim_cuis, gene_ids = load_converted_morbidmap()

	omim_tuples = set()
	for dmim, cuis in dmim_cuis.items():
		omim_tuples |= (set([(geneID, cui) for cui in cuis
			for geneID in gene_ids[dmim]]))

	return omim_tuples
