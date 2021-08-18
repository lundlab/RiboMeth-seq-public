#!/usr/bin/python
from sys import argv
import statistics
import re

fsamone = open(argv[1], "r")
fsamtwo = open(argv[2], "r")
fsamthr = open(argv[3], "r")
ffa = open(argv[4], "r")

my_trans = {}

my_one_read_count = 0
for line in fsamone:
	lineel = line.split()
	if lineel[0] == '@SQ':
		my_trans[lineel[1][3:]]= [int(lineel[2][3:]), 0, 0, 0, '']
	if lineel[1] == '16':
		my_one_read_count += 1
	if lineel[1] in ['16', '272']:
		my_trans[lineel[2]][1] += 1

my_two_read_count = 0
for line in fsamtwo:
	lineel = line.split()
	if lineel[1] == '16':
		my_two_read_count += 1
	if lineel[1] in ['16', '272']:
		my_trans[lineel[2]][2] += 1

my_three_read_count = 0
for line in fsamthr:
	lineel = line.split()
	if lineel[1] == '16':
		my_three_read_count += 1
	if lineel[1] in ['16', '272']:
		my_trans[lineel[2]][3] += 1


for line in ffa:
	if line[0:1] == '>':
		lineel = line.split()
		try:
			my_trans[lineel[0][1:]][4] = line[1:].rstrip()
		except KeyError:
			pass





print 'Transcript\tFull_name\tLength\t', 'rawReads_'+re.split('/|\.',argv[1])[-9], '\t', 'rawReads_'+re.split('/|\.',argv[2])[-9], '\t', 'rawReads_'+re.split('/|\.',argv[3])[-9], '\t', "rawReads_average", '\t', "rawReads_stdev", '\t', 'RPKM_'+re.split('/|\.',argv[1])[-9], '\t', 'RPKM_'+re.split('/|\.',argv[2])[-9], '\t', 'RPKM_'+re.split('/|\.',argv[3])[-9], '\t', 'RPKM_average', '\t', 'RPKM_average_stdev'

print 'Total\t\t\t', my_one_read_count, '\t', my_two_read_count, '\t', my_three_read_count, '\t'

for key in sorted(my_trans):
	#my_total = int(my_trans[key][1]) + int(my_trans[key][2]) + int(my_trans[key][3])

    my_read_average = int(((my_trans[key][1] + my_trans[key][2] + my_trans[key][3])/3))
    my_read_stdev = statistics.stdev([my_trans[key][1], my_trans[key][2], my_trans[key][3]])
    my_one_read_RPKM = (int(my_trans[key][1])*1000000000)/(my_one_read_count * my_trans[key][0])
    my_two_read_RPKM = (int(my_trans[key][2])*1000000000)/(my_two_read_count * my_trans[key][0])
    my_three_read_RPKM = (int(my_trans[key][3])*1000000000)/(my_three_read_count * my_trans[key][0])
    my_RPKM_average = (my_one_read_RPKM + my_two_read_RPKM + my_three_read_RPKM)/3
    my_stdev = statistics.stdev([my_one_read_RPKM, my_two_read_RPKM, my_three_read_RPKM])

    print key, '\t', my_trans[key][4], '\t', my_trans[key][0], '\t', my_trans[key][1], '\t', my_trans[key][2], '\t', my_trans[key][3], '\t', my_read_average, '\t', my_read_stdev, '\t', my_one_read_RPKM, '\t', my_two_read_RPKM, '\t', my_three_read_RPKM, '\t', my_RPKM_average, '\t', my_stdev
