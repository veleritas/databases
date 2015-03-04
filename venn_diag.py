# 2015-03-04 toby
"""
Generates information about the three way Venn diagram between
OMIM, SemMedDB, and Implicitome. Counts the overlapping information
between these databases by doing pair matching.
"""
import os
HOME = os.path.expanduser("~")

import sys
sys.path.append(os.path.join(HOME, "databases/omim"))
from parse_morbidmap import parse_morbidmap
from get_omim_tuples import load_converted_morbidmap

sys.path.append(os.path.join(HOME, "global_util"))
from file_util import read_file

sys.path.append(os.path.join(HOME, "databases/implicitome"))
from get_implicitome_tuples import all_imp_tuples

#-------------------------------------------------------------------------------
dmim_cuis, gene_ids = load_converted_morbidmap()

omim_tuples = dict()
for dmim, cuis in dmim_cuis.items():
	omim_tuples[dmim] = set([(gid, cui) for cui in cuis for gid in gene_ids[dmim]])

#-------------------------------------------------------------------------------

def get_all_omim_tuples():
	all_omim_tuples = set()
	for dmim in dmim_cuis.keys():
		all_omim_tuples |= omim_tuples[dmim]

	return all_omim_tuples

def omim_info():
	genes = parse_morbidmap()
	tuples = set()
	for dmim, gmims in genes.items():
		tuples |= set([(gmim, dmim) for gmim in gmims])

	print "number of unique indexable OMIM disease mims: {0}".format(len(genes))
	print "number of unique (gmim, dmim) pairs: {0}".format(len(tuples))

def compare_with_omim(tuples):
	ans = set()
	for dmim, o_tuples in omim_tuples.items():
		in_both = tuples & o_tuples
		temp = set([gid for gid, cui in in_both])
		ans |= set([(gid, dmim) for gid in temp])

	return ans

def get_semmed_tuples():
	"""Returns all semmeddb tuples"""
	semmed_tuples = set()
	loc = os.path.join(HOME, "global_util/semmeddb/data")
	for line in read_file("uniq_pred_agg.txt", loc):
		sub, s_type, pred, obj, o_type = line.split('\t')

		s_cuis = sub.split('|')
		o_cuis = obj.split('|')

		semmed_tuples |= set([(s, o) for s in s_cuis for o in o_cuis])

	return semmed_tuples

def main():
	all_omim_tuples = get_all_omim_tuples() # (gid, cui) format

	semmed_tuples = get_semmed_tuples() # all (sub, obj) pairs

	omim_and_sem = all_omim_tuples & semmed_tuples

#-------------------------------------------------------------------------------

	sem_and_omim = compare_with_omim(semmed_tuples) # count unique omim tuples

	print "omim intersect semmed, number of (gmim, dmim) pairs:", len(sem_and_omim)

	omim_and_imp = set()
	imp_and_sem = set()
	overlap_with_omim = set() # imp with omim
	overlap_with_sem = set() # imp with sem

#	now we loop through implicitome, and keep track of its overlap with the other two dbs
	i = 0
	for triple, i_gene_ids, i_cuis in all_imp_tuples():
		print i
		i += 1

		temp = set([(sub, obj) for sub in i_gene_ids for obj in i_cuis])
		and_omim = all_omim_tuples & temp
		and_sem = semmed_tuples & temp

		if len(and_omim) > 0:
			omim_and_imp |= and_omim
			overlap_with_omim.add(triple)

		if len(and_sem) > 0:
			imp_and_sem |= and_sem
			overlap_with_sem.add(triple)

#	print answers
	all_three_overlap = omim_and_sem & omim_and_imp & imp_and_sem
	print "# (gid, cui) pairs in all three overlap: {0}".format(len(all_three_overlap))
	print "# (sub, obj) pairs of omim and imp (imp ids): {0}".format(len(overlap_with_omim))
	print "# (sub, obj) pairs of sem and imp (imp ids): {0}".format(len(overlap_with_sem))

	sem_and_imp_minus_omim = imp_and_sem - all_omim_tuples
	sem_and_omim_minus_imp = omim_and_sem - omim_and_imp
	imp_and_omim_minus_sem = omim_and_imp - sem_and_omim

	print "#(gid, cui) pairs for sem & imp - omim {0}".format(len(sem_and_imp_minus_omim))
	print "#(gid, cui) pairs for omim & sem - imp {0}".format(len(sem_and_omim_minus_imp))
	print "#(gid, cui) pairs for omim & imp - sem {0}".format(len(imp_and_omim_minus_sem))

#---------------------
#	printing to files
	with open("./ans/all_3_overlap.txt", "w") as out:
		out.write("entrez_geneid|umls_cui\n")
		for val in all_three_overlap:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/sem_and_imp_minus_omim.txt", "w") as out:
		out.write("entrez_geneid|umls_cui\n")
		for val in sem_and_imp_minus_omim:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/imp_and_omim_minus_sem.txt", "w") as out:
		out.write("entrez_geneid|umls_cui\n")
		for val in imp_and_omim_minus_sem:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/sem_and_omim_minus_imp.txt", "w") as out:
		out.write("entrez_geneid|umls_cuis\n")
		for val in sem_and_omim_minus_imp:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/sem_and_imp_orig_ids.txt", "w") as out:
		out.write("tuple_id|subject_id|object_id\n")
		for val in overlap_with_sem:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/omim_and_imp_orig_ids.txt", "w") as out:
		out.write("tuple_id|subject_id|object_id\n")
		for val in overlap_with_omim:
			out.write("{0}\n".format("|".join(val)))

	with open("./ans/imp_and_sem_minus_omim_orig_ids.txt", "w") as out:
		out.write("tuple_id|subject_id|object_id\n")
		temp = overlap_with_sem - overlap_with_omim
		for val in temp:
			out.write("{0}\n".format("|".join(val)))

if __name__ == "__main__":
	main()
