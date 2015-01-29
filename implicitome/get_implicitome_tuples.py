# last updated 2015-01-29 toby
import mysql.connector
import const

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from read_ids import read_ids

import os

def get_db_raw_tuples(tuple_id_range):
#	returns all tuples with min_percentile <= percentile <= max percentile
#	also returns the tuple_id for easy indexing

	cnx = mysql.connector.connect(database = "implicitome",
		**const.DB_INFO)

	if cnx.is_connected():
		cur = cnx.cursor()

		query = ("SELECT tuple_id, sub_id, obj_id FROM tuples "
			"WHERE tuple_id BETWEEN %s AND %s;")

		cur.execute(query, (tuple_id_range[0], tuple_id_range[1]))

		raw_tuples = set()
		for row in cur:
			raw_tuples.add((row[0], row[1], row[2]))

		cur.close()

	cnx.close()
	return raw_tuples

def cache_filename(tuple_id_range):
	cache_loc = "/home/toby/databases/implicitome/data/"
	return cache_loc + str(tuple_id_range[0]) + "_" + str(tuple_id_range[1]) + ".txt"

def get_raw_tuples(tuple_id_range):
	fname = cache_filename(tuple_id_range)
	if os.path.exists(fname):
		print "reading from cache"
		raw_tuples = set()
		for line in read_file(fname):
			tuple_id, sub_id, obj_id = line.split("|")
			raw_tuples.add((tuple_id, sub_id, obj_id))

		return raw_tuples

#	otherwise query, cache, and return
	print "querying"
	raw_tuples = get_db_raw_tuples(tuple_id_range)
	print "caching"
	with open(fname, "w") as out:
		for raw_tuple in raw_tuples:
			out.write("{0}|{1}|{2}\n".format(raw_tuple[0], raw_tuple[1], raw_tuple[2]))

	return raw_tuples

def get_implicitome_tuples(tuple_id_range = (1, 10000)):
	raw_tuples = get_raw_tuples(tuple_id_range)

	sub_ids, obj_ids = read_ids()

	implicitome_tuples = set()
	for triple in raw_tuples:
#		first value is tuple id
		sub = triple[1]
		obj = triple[2]

		if "EG" in sub_ids[sub] and "UMLS" in obj_ids[obj]:
			gene_ids = sub_ids[sub]["EG"]
			cuis = obj_ids[obj]["UMLS"]

			implicitome_tuples |= set([(gid, cui) for gid in gene_ids for cui in cuis])

	return implicitome_tuples

def main():
	print "getting tuples"
	tuples = get_raw_tuples((1, 80000000))
	print len(tuples)
	print "done"

if __name__ == "__main__":
	main()
