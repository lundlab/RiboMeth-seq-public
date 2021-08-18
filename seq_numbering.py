#!/usr/bin/python
from sys import argv
fsequence = open(argv[1], "r")
fdata = open(argv[2], "r")

datadic = {}
seqdic={}
for line in fsequence:
	x=0
	if line[0:1] == '>':
		lineel=line.split()
		name=lineel[0][1:]
		seqdic[name]=''
	else:
		line=line.replace('a','A')
		line=line.replace('g','G')
		line=line.replace('c','C')
		line=line.replace('T','U')
		line=line.replace('t','U')
		seqdic[name]+=line.rstrip()


for line in fdata:
	lineel=line.split()
	try:
		print ' '.join( [lineel[0], lineel[1], seqdic[lineel[0]][int(lineel[1])-1], lineel[2], lineel[3], lineel[4], lineel[5], lineel[6], lineel[7] ])
	except KeyError:
		print line.rstrip()
