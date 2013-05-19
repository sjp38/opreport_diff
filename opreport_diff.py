#!/usr/bin/env python

import sys

def analyze_opreport(filename):
	result = {}
	for line in open(filename):
		try:
			spltd = line.split()
			try:
				int(spltd[0])
			except ValueError:
				continue
			result[spltd[4]] = spltd[1]
		except IndexError:
			pass
	return result


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <report file 1> <report file 2> .." % sys.argv[0]
		sys.exit()
	num_of_option = 0
	CSV_FORMAT = False
	if "--csv" in sys.argv:
		num_of_option = num_of_option + 1
		CSV_FORMAT = True

	analyzed_results = []
	for filename in sys.argv[num_of_option + 1:]:
		analyzed_results.append(analyze_opreport(filename))

	diffs = {}
	for funcname in analyzed_results[0]:
		diff = []
		for result in analyzed_results:
			diff.append(result.get(funcname, "0.0"))
		key = abs(float(diff[0]) - float(diff[-1]))
		diff.append(funcname)
		diffs[key] = diff

	file_name_header = "diff files: "
	func_name_delim = ":\n\t"
	percent_delim = " -> "

	if CSV_FORMAT:
		file_name_header = "file name,"
		func_name_delim = ','
		percent_delim = ','
	print "%s%s" % (file_name_header,
			percent_delim.join(sys.argv[num_of_option + 1:]))

	for diff_abs in sorted(diffs, reverse=True):
		diff = diffs[diff_abs]
		func_name = diff[-1]
		if CSV_FORMAT:
			func_name = func_name.split(',')[0]
		print "%s%s%s" % (func_name, func_name_delim,
				percent_delim.join(diff[0:-1]))
