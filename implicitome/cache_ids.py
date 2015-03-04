# last updated 2015-03-03 toby
"""
Converts all unique implicitome subject and object identifiers
to UMLS CUIs or OMIM identifiers.

Uses database left joins to perform this task in bulk.
"""
import mysql.connector
import const

import sys
sys.path.append("/home/toby/global_util/")
import check

import time

def query_implicitome(query):
	cnx = mysql.connector.connect(**const.DB_INFO)
	if cnx.is_connected():
		cur = cnx.cursor()

		cur.execute(query)
		for row in cur:
			yield row

		cur.close()
	cnx.close()

def cache_sub_ids():
	"""
	Converts implicitome identifiers to Entrez gene IDs or OMIM
	ids ("mims"). Caches the information to a file.
	"""
	query = ("SELECT uniq_table.sub_id, dblink.dbid, dblink.id "
		"FROM (SELECT DISTINCT sub_id FROM tuples) "
		"AS uniq_table "
		"LEFT JOIN dblink "
		"ON uniq_table.sub_id = dblink.conceptid "
		"WHERE dblink.dbid IN ('OM', 'EG');")

	with open("uniq_sub_id_converted.txt", "w") as out:
		for row in query_implicitome(query):
			if row[1] == "EG" or row[1] == "OM" and check.is_mim(row[2]):
				out.write("{0}|{1}|{2}\n".format(row[0], row[1], row[2]))

def cache_obj_ids():
	"""
	Converts implicitome identifiers to OMIM ids or UMLS
	CUIs. Caches the information to a file.
	"""
	query = ("SELECT uniq_table.obj_id, dblink.dbid, dblink.id "
		"FROM (SELECT DISTINCT obj_id FROM tuples) "
		"AS uniq_table "
		"LEFT JOIN dblink "
		"ON uniq_table.obj_id = dblink.conceptid "
		"WHERE dblink.dbid IN ('OM', 'UMLS');")

	with open("uniq_obj_id_converted.txt", "w") as out:
		for row in query_implicitome(query):
			if ((row[1] == "OM" and check.is_mim(row[2])) or
				(row[1] == "UMLS" and check.is_cui(row[2]))):
				out.write("{0}|{1}|{2}\n".format(row[0], row[1], row[2]))

def main():
	print "working"
	start_time = time.time()
	print "working on subjects"
	cache_sub_ids()
	print "working on objects"
	cache_obj_ids()
	stop_time = time.time()

	print "the program took {0} seconds to run".format(stop_time - start_time)

if __name__ == "__main__":
	main()
	print "done"
