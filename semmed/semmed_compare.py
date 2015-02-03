# last updated 2015-01-29 toby
import sys
sys.path.append("/home/toby/databases/omim/")

from get_omim_tuples import load_converted_morbidmap
from get_semmed_tuples import get_semmed_tuples
from collections import defaultdict

from dmim_name import read_omim_names

dmim_name = read_omim_names()

dmim_cuis, gene_ids = load_converted_morbidmap()

def compare_with_omim(db_tuples):
#	set of (gid, dmim)
	omim_only = set()
	in_both = set()

	for dmim, cuis in dmim_cuis.items():
		gids = gene_ids[dmim]
		subtuples = set([(gid, cui) for gid in gids for cui in cuis])

		intersection = subtuples & db_tuples

		uniq = set([val[0] for val in intersection])

		in_both |= set([(gid, dmim) for gid in uniq])
		omim_only |= set([(gid, dmim) for gid in gids if gid not in uniq])

	return (omim_only, in_both)

def main():
#	compare omim with semmeddb
	semmed_tuples, name, identifers = get_semmed_tuples()

#	find things definitely not in omim
	all_omim_tuples = set()
	for dmim, cuis in dmim_cuis.items():
		all_omim_tuples = set([(gid, cui) for cui in cuis for gid in gene_ids[dmim]])

	semmed_only = semmed_tuples - all_omim_tuples

	counts = defaultdict(int)
	for val in semmed_only:
		counts[val[1]] += 1

	cuis = [(val, num) for val, num in counts.items()]
	cuis = sorted(cuis, key = lambda x: x[1], reverse = True)

	with open("semmed_minus_omim_cuis.txt", "w") as out:
		for cui, num in cuis:
			out.write("{0}|{1}|{2}\n".format(cui, num, name[cui]))


#	compare with omim, and output the dmims?


	omim_only, in_both = compare_with_omim(semmed_tuples)

	print "size omim only", len(omim_only)
	print "size in both", len(in_both)

	counts = defaultdict(int)
	for gid, dmim in omim_only:
		counts[dmim] += 1

	dmims = [(dmim, num) for dmim, num in counts.items()]
	dmims = sorted(dmims, key = lambda x: x[1], reverse = True)

	with open("omim_minus_semmed.txt", "w") as out:
		for dmim, num in dmims:
			out.write("{0}|{1}|{2}\n".format(dmim, num, dmim_name[dmim]))

	counts = defaultdict(int)
	for gid, dmim in in_both:
		counts[dmim] += 1

	dmims = [(dmim, num) for dmim, num in counts.items()]
	dmims = sorted(dmims, key = lambda x: x[1], reverse = True)

	with open("omim_and_semmed.txt", "w") as out:
		for dmim, num in dmims:
			out.write("{0}|{1}|{2}\n".format(dmim, num, dmim_name[dmim]))




if __name__ == "__main__":
	main()
	print "done"
