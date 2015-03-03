# last updated 2015-03-02 toby
"""
Converts OMIM gene and disease identifiers into Entrez gene IDS
and UMLS CUIs.
"""
from parse_morbidmap import parse_morbidmap

def main():
	bad_dmims = set()
	genes = parse_morbidmap()
	with open("./data/converted_morbidmap2.txt", "w") as out:
		for dmim, gmims in sorted(genes.items()):
			cuis = convert.dmim_to_cui(dmim)
			if not cuis:
				bad_dmims.add(dmim)




			gene_ids = set()
			for gmim in gmims:
				gene_id = convert.gmim_to_geneID(gmim)
				if temp:
					gene_ids.add(gene_id)

			out.write("{0}|{1}\n".format(dmim, "|".join(cuis)))
			out.write("\t{0}\n".format("|".join(gene_ids)))


















from parse_morbidmap import parse_morbidmap

import sys
sys.path.append("/home/toby/global_util/")
import convert
from file_util import read_file

def main():
#	mm_loc = "/home/toby/databases/omim/data/"

	bad_dmims = set()
	with open("./data/converted_morbidmap.txt", "w") as out:
		for line in read_file("./data/sorted_morbidmap.txt"):
			line = line.lstrip('#')
			vals = line.split('|')

			dmim = vals[0]
			gmims = vals[1:]

			cuis = convert.dmim_to_cui(dmim)
			if not cuis:
				bad_dmims.add(dmim)

			gene_ids = set()
			for gmim in gmims:
				temp = convert.gmim_to_geneID(gmim)
				if temp:
					gene_ids.add(temp)

			print "dmim", dmim

#			print to file
			out.write(dmim)
			for cui in cuis:
				out.write("|" + cui)
			out.write('\n')

			out.write('\t')
			for j, gid in enumerate(gene_ids):
				out.write(gid)
				if j < len(gene_ids) - 1:
					out.write('|')
			out.write('\n')

	with open("bad_dmims.txt", "w") as out:
		for val in bad_dmims:
			out.write(val + "\n")

if __name__ == "__main__":
	main()
	print "done"
