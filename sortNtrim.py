#!/usr/bin/python
from sys import argv

script, data, barcode = argv
fin = open(argv[1], "r")


i = 0
keep = 0
okreads = 0 #Counter of reads with barcode
BC = argv[2] #Barcode to search the read for
read_dic = []

for line in fin:
	i = i+1
	if ((i-1)%4)==0: #identifies read name line
		name = line
	if ((i-2)%4)==0: #identifies read sequence line
		barcode = line[0:len(BC)]	#Defines the barcode segment of read
		if barcode != BC:
			keep = 0
		else:
			line = line[len(BC):]	#Number of nucleotides to trim from read
			okreads +=1
			keep = 1
			read_dic.append(name)
			read_dic.append(line[0:])
			read_dic.append('+' +'\n')
	if ((i-4)%4)==0 and keep==1:
		read_dic.append(line[len(BC):])	#Number of nucleotides to trim from read

#f = open('data.BC.fq', 'w')
for line in read_dic:
	print line.rstrip()
#f.close()

#print 'Total reads:			%s' % (i/4)
#print 'Reads with barcodes:		%s	written to file %s' % (okreads, 'data.BC.fq')
