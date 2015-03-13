# last updated 2015-03-12 toby
"""
Returns implicitome information in either its raw state
or its converted format. The details of dealing with the
large amount of implicitome information is abstracted
out to this function. This prevents loading of the entire
database into memory (~25 GB).
"""
import logging
import mysql.connector
import os

import sys
sys.path.append("/home/toby/global_util/")
import DB_LOGINS as DB
from file_util import read_file
from read_ids import read_ids
from file_util import exists

def get_db_raw_tuples(tuple_id_range):
	"""
	Queries the implicitome database for implicitome tuples
	within a specific range.
	"""
	cnx = mysql.connector.connect(database = "implicitome", **DB.AVALANCHE)
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
	"""
	Gives the filename of a cached implicitome block.
	"""
	cache_loc = "/home/toby/databases/implicitome/data/"
	return cache_loc + str(tuple_id_range[0]) + "_" + str(tuple_id_range[1]) + ".txt"

def read_cached_tuples(fname):
	"""
	Reads a cached implicitome block of information.
	Assumes that the block exists. (Check for existence
	is performed by get_raw_tuples()).
	"""
	logging.debug("Reading from cache")
	raw_tuples = set()
	for line in read_file(fname):
		tuple_id, sub_id, obj_id = line.split('|')
		raw_tuples.add((tuple_id, sub_id, obj_id))

	return raw_tuples

def get_raw_tuples(tuple_id_range):
	"""
	Actually gives the raw implicitome information using one
	of two methods:

	1. Reads the information from disk if it exists.
	2. If no cached version is available, reads directly from
		the database and then caches to disk for next time.
	"""
	fname = cache_filename(tuple_id_range)
	if not exists(fname):
		logging.debug("Querying implicitome with tuple range {0}".format(tuple_id_range))
		raw_tuples = get_db_raw_tuples(tuple_id_range)
		with open(fname, "w") as out:
			for raw_tuple in raw_tuples:
				out.write("{0}|{1}|{2}\n".format(raw_tuple[0], raw_tuple[1], raw_tuple[2]))

	return read_cached_tuples(fname)

def all_imp_tuples(tuple_id_range = (1, 205000000)):
	"""
	Used for looping through all of implicitome one row at a time
	because holding the entire database in memory is too RAM intensive.

	The function returns one row along with the information in that row
	converted to Entrez gene IDs and UMLS CUIs.

	The program speeds up the process by processing implicitome in
	chunks, and saves each chunk to disk so that it only ever has to
	query the database for each chunk once. Chunk size is arbitrary.
	"""
	CHUNK_SIZE = 50000
	cur_val = tuple_id_range[0]

	sub_ids, obj_ids = read_ids()

	while cur_val < tuple_id_range[1]:
		cur_range = (cur_val, cur_val + CHUNK_SIZE + 1)

		raw_tuples = get_raw_tuples(cur_range)
		for value in raw_tuples:
			sub = value[1]
			obj = value[2]
			if "EG" in sub_ids[sub] and "UMLS" in obj_ids[obj]:
				gene_ids = sub_ids[sub]["EG"]
				cuis = obj_ids[obj]["UMLS"]
				yield (value, gene_ids, cuis)

		cur_val += CHUNK_SIZE

def all_links_of_type(link_type):
	"""
	Returns all the gene-disease links of a certain kind (explicit
	or implicit).
	"""
	assert link_type in ["implicit", "explicit"], "bad choice for implicitome links"
	loc = "/home/toby/databases/implicitome/"
	fname = "{0}_links.txt".format(link_type)

	sub_ids, obj_ids = read_ids()
	for line in read_file(fname, loc):
		sub, obj, score = line.split("|")
		if "EG" in sub_ids[sub] and "UMLS" in obj_ids[obj]:
			gene_ids = sub_ids[sub]["EG"]
			cuis = obj_ids[obj]["UMLS"]
			yield ((sub, obj), gene_ids, cuis)








def get_implicitome_tuples(tuple_id_range = (1, 10000)):
	"""
	Returns a certain range of implicitome information based on
	the tuple id. The information is converted to UMLS CUIs and
	Entrez gene IDs.
	"""
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
