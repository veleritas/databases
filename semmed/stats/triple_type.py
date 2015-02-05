import sys
sys.path.append("/home/toby/databases/semmed/")
sys.path.append("/home/toby/global_util/")
from file_util import read_file

from collections import defaultdict
import const

import mysql.connector

import time

def query():
	cnx = mysql.connector.connect(**const.DB_INFO)

	ans = set()
	if cnx.is_connected():
		cur = cnx.cursor()
		query = ("SELECT DISTINCT s_cui, s_type, predicate, "
			"o_cui, o_type "
			"FROM PREDICATION_AGGREGATE;")
#	makes the file "wow.txt"

		print "querying db"
		cur.execute(query)
		print "reading data"
		for row in cur:
			ans.add((row[0], row[1], row[2], row[3], row[4]))

		cur.close()
	cnx.close()
	return ans

def main():
#	temp = query()

#	split up and count with respect to type
	print "counting"
	count = defaultdict(int)

	uniq_tuples = defaultdict(set)
	for line in read_file("wow.txt"):
		sub, s_type, pred, obj, o_type = line.split('\t')
		s_cuis = sub.split('|')
		o_cuis = obj.split('|')
		tripls = set([(s, pred, o) for s in s_cuis for o in o_cuis])


		count[(s_type, pred, o_type)] += len(tripls)

		uniq_tuples[(s_type, pred, o_type)] |= set([(s, o) for s in s_cuis for o in o_cuis])

#	for val in temp:
#		sub = val[0]
#		obj = val[3]
#		pred = val[2]
#		s_type = val[1]
#		o_type = val[4]
#
#		s_cuis = sub.split('|')
#		o_cuis = obj.split('|')
#
#		trips = set([(s, pred, o) for s in s_cuis for o in o_cuis])
#		for s, p, o in trips:
#			count[(s_type, pred, o_type)] += 1

	print "caching"

	ans = [(v, num) for v, num in count.items()]
	ans = sorted(ans, key = lambda x: x[1], reverse = True)

	with open("triple_types.txt", "w") as out:
		for v, num in ans:
			s = v[0]
			p = v[1]
			o = v[2]
			out.write("{0}|{1}|{2}|{3}\n".format(s, p, o, num))

if __name__ == "__main__":
	start_time = time.time()
	main()
	stop_time = time.time()
	print "total runtime {0} sec".format(stop_time - start_time)
	print "done"
