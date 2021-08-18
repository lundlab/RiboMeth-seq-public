#!/usr/bin/python
from sys import argv
fin = open(argv[1], "r")

mapped=0
unmap=0

for line in fin:
	lineel = line.split()
	if lineel[1] =='16':
		mapped += 1
	elif lineel[1] =='4':
		unmap+=1

import os
print argv[1]
print 'Total_number_of_reads', unmap+mapped
print 'Mapped_reads', mapped, (float(mapped)/(float(unmap)+float(mapped)))*100.0 ,'%'

