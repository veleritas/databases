# last updated 2015-01-27 toby
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

def read_ids():
	indir = "/home/toby/databases/implicitome/data/"

	sub_ids = dict()
	for line in read_file("uniq_sub_id_converted.txt", indir):
		sub_id, id_type, id_val = line.split('|')

		if sub_id not in sub_ids:
			sub_ids[sub_id] = {}

		if id_type not in sub_ids[sub_id]:
			sub_ids[sub_id][id_type] = set()

		sub_ids[sub_id][id_type].add(id_val)

	obj_ids = dict()
	for line in read_file("uniq_obj_id_converted.txt", indir):
		obj_id, id_type, id_val = line.split('|')

		if obj_id not in obj_ids:
			obj_ids[obj_id] = {}

		if id_type not in obj_ids[obj_id]:
			obj_ids[obj_id][id_type] = set()

		obj_ids[obj_id][id_type].add(id_val)

	return (sub_ids, obj_ids)
