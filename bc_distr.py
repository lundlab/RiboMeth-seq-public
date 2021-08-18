#!/usr/bin/python
from sys import argv
fin = open(argv[1],  "r")

i=0.0
bc=[]

for line in fin:
	i +=1
	if (i-2.0)/4.0 == int((i-2.0)/4.0):
		bc.append(line[0:6])
from collections import Counter
barcode = Counter(bc).most_common(50)

for j in barcode:
	line = ' '.join(str(x) for x in j)
	print line

