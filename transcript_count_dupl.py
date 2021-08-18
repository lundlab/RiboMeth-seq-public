#!/usr/bin/python
from sys import argv

fsamone = open(argv[1], "r")
fsamtwo = open(argv[2], "r")
ffa = open(argv[3], "r")

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

for line in ffa:
	if line[0:1] == '>':
		lineel = line.split()
		try:
			my_trans[lineel[0][1:]][4] = line[1:].rstrip()
		except KeyError:
			pass


my_read_count = my_one_read_count + my_two_read_count

print 'Transcript\tFull_name\tLength\t', argv[1].split('/')[-2], '\t', argv[2].split('/')[-2], '\tTotal_read-count\tExpression_RPKM'

print 'Total\t\t\t', my_one_read_count, '\t', my_two_read_count

for key in sorted(my_trans):
	my_total = int(my_trans[key][1]) + int(my_trans[key][2])
	
	print key, '\t', my_trans[key][4], '\t', my_trans[key][0], '\t', my_trans[key][1], '\t', my_trans[key][2], '\t', my_total, '\t' , round( (my_total*1000000000 / ( float(my_trans[key][0])*my_read_count) ) ,2)








































