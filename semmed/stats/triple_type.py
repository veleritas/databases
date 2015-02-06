# last updated 2015-02-06 toby
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

sys.path.append("/home/toby/databases/omim/")
from get_omim_tuples import load_converted_morbidmap
from collections import defaultdict

import time

#query = ("SELECT DISTINCT s_cui, s_type, predicate, "
#	"o_cui, o_type FROM PREDICATION_AGGREGATE;")
#	INTO OUTFILE '/tmp/wow.txt'

dmim_cuis, gene_ids = load_converted_morbidmap()

def compare_with_omim(tuples):
	ans = 0 # num hits found in omim
	for dmim, cuis in dmim_cuis.items():
		geneids = gene_ids[dmim]

		temp = set([(gid, cui) for cui in cuis for gid in geneids])
		in_both = temp & tuples
		uniq = set([gid for gid, cui in in_both])

		ans += len(uniq)

	return ans

def main():
#	split up and count with respect to type
	print "counting"
	count = defaultdict(int)
	uniq_tuples = defaultdict(set)
	for line in read_file("wow.txt"):
		sub, s_type, pred, obj, o_type = line.split('\t')
		s_cuis = sub.split('|')
		o_cuis = obj.split('|')

		tuples = set([(s, o) for s in s_cuis for o in o_cuis])

		count[(s_type, pred, o_type)] += len(tuples)
		uniq_tuples[(s_type, pred, o_type)] |= tuples

#	try to intersect with omim and look for hits
	intersect = dict()
	i = 0
	for trip, tups in uniq_tuples.items():
		print i
		intersect[trip] = compare_with_omim(tups)
		i += 1

	print "caching"

	ans = [(v, num) for v, num in count.items()]
	ans = sorted(ans, key = lambda x: x[1], reverse = True)

	with open("triple_types.txt", "w") as out:
		for v, num in ans:
			s = v[0]
			p = v[1]
			o = v[2]
			out.write("{0}|{1}|{2}|{3}|{4}\n".format(s, p, o, num, intersect[v]))

if __name__ == "__main__":
	start_time = time.time()
	main()
	stop_time = time.time()
	print "total runtime {0} sec".format(stop_time - start_time)
	print "done"
