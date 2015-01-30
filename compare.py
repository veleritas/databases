# last updated 2015-01-29 toby
import logging
from omim.get_omim_tuples import load_converted_morbidmap
from implicitome.get_implicitome_tuples import get_implicitome_tuples

dmim_cuis, gene_ids = load_converted_morbidmap()

def compare_with_omim(db_tuples):
#	compare the tuples of one database with omim
	num_in_omim = 0
	num_not_in_omim = 0

	for dmim, cuis in dmim_cuis.items():
		logging.debug("dmim {0}".format(dmim))

		gids = gene_ids[dmim]
		subtuples = set([(gid, cui) for gid in gids for cui in cuis])

		logging.debug("subtuples")
		logging.debug(subtuples)

		intersection = subtuples & db_tuples
		logging.debug("intersection")
		logging.debug(intersection)

		uniq = set([val[0] for val in intersection])

		logging.debug("uniq")
		logging.debug(uniq)


		num_in_omim += len(uniq)
		num_not_in_omim += len(gids) - len(uniq)

	return (num_in_omim, num_not_in_omim)

def main():
	logging.basicConfig(filename="lolol.log", level=logging.INFO)

	max_val = 205000000

	chunk_size = 50000

	cur_val = 1
	with open("ans.txt", "w") as out:
		out.write("imp_start,imp_stop,imp_size,in_omim,not_omim\n")

		while cur_val < max_val:
			tuple_range = (cur_val, cur_val + chunk_size -1)
			print tuple_range

			print "getting tuples"
			implicitome_tuples = get_implicitome_tuples(tuple_range)
			print "comparing tuples"
			num_in_omim, num_not_in_omim = compare_with_omim(implicitome_tuples)
			print "writing to file"
			out.write("{0},{1},{2},{3},{4}\n".format(cur_val, tuple_range[1], len(implicitome_tuples), num_in_omim, num_not_in_omim))
			cur_val += chunk_size




if __name__ == "__main__":
	main()
	print "done"
