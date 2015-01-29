# last updated 2015-01-29 toby
import mysql.connector
import const
from collections import defaultdict

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from file_util import exists
import check

import os

def cache_db_query(outloc):
#	querys database for gene-disease links and caches to file

	cnx = mysql.connector.connect(**const.DB_INFO)
	if cnx.is_connected():
		cur = cnx.cursor()

		query = ("SELECT DISTINCT PID, SID, PMID, "
			"s_cui, s_name, predicate, o_cui, o_name "
			"FROM PREDICATION_AGGREGATE "
			"WHERE s_type IN ('gngm', 'aapp') "
			"AND o_type IN ('dsyn', 'neop', 'cgab', 'mobd');")

		cur.execute(query)

		with open(os.path.join(outloc, "semmed_raw_info.txt"), "w") as out:
			for row in cur:
				out.write("{0}#{1}#{2}#{3}#".format(row[0], row[1], row[2], row[3]))
				out.write("{0}#{1}#{2}#{3}\n".format(row[4], row[5], row[6], row[7]))

		cur.close()

	cnx.close()

def read_cached_info(inloc):
#	reads the cached raw semmeddb info
#	and returns a set of unique tuples

	semmed_tuples = set()
	name = dict()
	identifiers = defaultdict(list)

	for line in read_file("semmed_raw_info.txt", inloc):
		vals = line.split('#')

#		obj_cui are all C1234567 (no gene ids)
		sub_ids = vals[3].split('|')
		sub_names = vals[4].split('|')

		assert check.is_cui(vals[6]), "not a cui! PID {0} s_cui {1}".format(vals[0], vals[6])

		semmed_tuples |= set([(val, vals[6]) for val in sub_ids])

		for val in sub_ids:
			identifiers[(val, vals[6])].append((vals[5], vals[0], vals[1], vals[2]))

		name[vals[6]] = vals[7]
		for sub, s_name in zip(sub_ids, sub_names):
			name[sub] = s_name

	return (semmed_tuples, name, identifiers)

def get_semmed_tuples():
	inloc = "/home/toby/databases/semmed/data"
	if not exists("semmed_raw_info.txt", inloc):
		cache_db_query(inloc)

	return read_cached_info(inloc)
