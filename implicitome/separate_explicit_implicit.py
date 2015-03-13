# last updated 2015-03-12 toby
"""
Splits implicitome gene-disease links into explicit and implicit
sets (explicit = in a pubmed paper, implicit = not in a paper).
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
import time

def main():
	loc = "/home/toby/implicitome/orig_data/"
	fname = "matchscores.txt-coOcc-no-NaN.txt"
	print "working"
	with open("explicit_links.txt", "w") as explicit:
		with open("implicit_links.txt", "w") as implicit:
			for line in read_file(fname, loc):
				vals = line.split(',', 3)
				assert len(vals) == 4, "{0}".format("|".join(vals))
				if vals[3] == "[]": # implicit
					implicit.write("{0}\n".format("|".join(vals[:-1])))
				else: # explicit
					explicit.write("{0}\n".format("|".join(vals[:-1])))

if __name__ == "__main__":
	start_time = time.time()
	main()
	stop_time = time.time()
	print "took {0} s".format(stop_time - start_time)
