# last updated 2015-01-27 toby

from parse_morbidmap import parse_morbidmap

import sys
sys.path.append("/home/toby/global_util/")
import convert
from file_util import read_file

def main():
	genes = parse_morbidmap()
	dmims = sorted(list(genes))

	N = len(dmims)

	bad_dmims = []
	bad_gmims = []
	outloc = "/home/toby/databases/omim/"
	with open(outloc + "converted_morbidmap.txt", "w") as out:
		for i, dmim in enumerate(dmims):
			print "{0}/{1}, {2}".format(i+1, N, dmim)

			cuis = convert.dmim_to_cui(dmim)
			if not cuis:
				bad_dmims.append(dmim)

			print "cuis", cuis

			gmims = genes[dmim]
			temp_ids = map(convert.gmim_to_geneID, gmims)

			print "gene ids", temp_ids

			gene_ids = []
			for sublist, gmim in zip(temp_ids, gmims):
				gene_ids += sublist
				if len(sublist) == 0 or len(sublist) > 1:
					bad_gmims.append((gmim, sublist))


			out.write(dmim)
			for cui in cuis:
				out.write("|" + cui)
			out.write('\n')

			out.write("\t")
			for j, gid in enumerate(gene_ids):
				out.write(gid)
				if j < len(gene_ids) - 1:
					out.write("|")
			out.write("\n")

	with open(outloc + "bad_dmims.txt", "w") as out:
		for dmim in bad_dmims:
			out.write(dmim + "\n")

	with open(outloc + "bad_gmims.txt", "w") as out:
		for gmim, sublist in bad_gmims:
			out.write("gmim " + gmim + "\n")
			out.write(str(sublist) + "\n")

if __name__ == "__main__":
	main()
