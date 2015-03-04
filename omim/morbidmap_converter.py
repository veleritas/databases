# last updated 2015-03-02 toby
"""
Converts OMIM gene and disease identifiers into Entrez gene IDS
and UMLS CUIs.
"""
import os
HOME = os.path.expanduser("~")

import sys
sys.path.append(os.path.join(HOME, "global_util"))
import convert
from parse_morbidmap import parse_morbidmap

def main():
	bad_dmims = set()
	genes = parse_morbidmap()
	with open("./data/converted_morbidmap.txt", "w") as out:
		for dmim, gmims in sorted(genes.items()):
			print "dmim: {0}".format(dmim)

			cuis = convert.dmim_to_cui(dmim)
			if not cuis:
				bad_dmims.add(dmim)

			gene_ids = set()
			for gmim in gmims:
				gene_id = convert.gmim_to_geneID(gmim)
				if gene_id:
					gene_ids.add(gene_id)

			out.write("{0}|{1}\n".format(dmim, "|".join(cuis)))
			out.write("\t{0}\n".format("|".join(gene_ids)))

#	OMIM disease identifers with no associated UMLS CUI
	with open("./data/bad_dmims.txt", "w") as out:
		for val in bad_dmims:
			out.write("{0}\n".format(val))

if __name__ == "__main__":
	main()
	print "done"
