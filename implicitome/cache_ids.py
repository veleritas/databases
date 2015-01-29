# last updated 2015-01-27 toby
import mysql.connector
import const

import sys
sys.path.append("/home/toby/global_util/")
import check

import time

def cache_sub_ids():
	cnx = mysql.connector.connect(database = "implicitome",
		**const.DB_INFO)

	if cnx.is_connected():
		cur = cnx.cursor()

		query = ("SELECT uniq_table.sub_id, dblink.dbid, dblink.id "
			"FROM (SELECT DISTINCT sub_id FROM tuples) "
			"AS uniq_table "
			"LEFT JOIN dblink "
			"ON uniq_table.sub_id = dblink.conceptid "
			"WHERE dblink.dbid IN ('OM', 'EG');")

		cur.execute(query)

		with open("uniq_sub_id_converted.txt", "w") as out:
			for row in cur:
				if row[1] == "EG" or row[1] == "OM" and check.is_mim(row[2]):
					out.write("{0}|{1}|{2}\n".format(row[0], row[1], row[2]))

		cur.close()
	cnx.close()

def cache_obj_ids():
	cnx = mysql.connector.connect(database = "implicitome",
		**const.DB_INFO)

	if cnx.is_connected():
		cur = cnx.cursor()

		query = ("SELECT uniq_table.obj_id, dblink.dbid, dblink.id "
			"FROM (SELECT DISTINCT obj_id FROM tuples) "
			"AS uniq_table "
			"LEFT JOIN dblink "
			"ON uniq_table.obj_id = dblink.conceptid "
			"WHERE dblink.dbid IN ('OM', 'UMLS');")

		cur.execute(query)

		with open("uniq_obj_id_converted.txt", "w") as out:
			for row in cur:
				if row[1] == "OM" and check.is_mim(row[2]):
					out.write("{0}|{1}|{2}\n".format(row[0], row[1], row[2]))
				elif row[1] == "UMLS" and check.is_cui(row[2]):
					out.write("{0}|{1}|{2}\n".format(row[0], row[1], row[2]))

		cur.close()
	cnx.close()

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
