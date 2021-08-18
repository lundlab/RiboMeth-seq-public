#!/usr/bin/python
from sys import argv
fin = open(argv[1], "r")

first_read_NM = ''

for line in fin:
	lineel = line.split()
	if len(lineel) > 10:
		if lineel[1] == '16':
			print line.rstrip()
			
			first_read_NM = int(line.split('NM:i:')[1].split()[0])
		if lineel[1] == '272' and int(line.split('NM:i:')[1].split()[0]) <= first_read_NM:
			print line.rstrip()

		if lineel[1] == '0':
			print line.rstrip()
			
			first_read_NM = int(line.split('NM:i:')[1].split()[0])
		if lineel[1] == '256' and int(line.split('NM:i:')[1].split()[0]) <= first_read_NM:
			print line.rstrip()


	else:
		print line.rstrip()
