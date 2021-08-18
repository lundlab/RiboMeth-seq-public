#!/usr/bin/python
from sys import argv
fin = open(argv[1], "r")

import math
import os
my_dir = os.getcwd().split('/')


combdic = {}
fone = open(argv[1],  "r")
ftwo = open(argv[2],  "r")

next(fone)
for line in fone:
	lineel=line.split()
	combdic[lineel[0]] = combdic.get(lineel[0], {})
	combdic[lineel[0]][int(lineel[1])] = lineel[2], lineel[3], lineel[9], lineel[10], lineel[11], lineel[12]
	
next(ftwo)
for line in ftwo:
	lineel=line.split()
	if combdic[lineel[0]][int(lineel[1])][0] == 'No_cov' and lineel[2] != 'No_cov':
		combdic[lineel[0]][int(lineel[1])] = lineel[2], 0,0,0,0,0, lineel[3], lineel[9], lineel[10], lineel[11], lineel[12]
	else:	
		combdic[lineel[0]][int(lineel[1])] += lineel[3], lineel[9], lineel[10], lineel[11], lineel[12]


print "Subunit Position Nucleotide Tot_Cov Tot_Cov G% A% T% C% G_std_dev A_std_dev T_std_dev C_std_dev Above_2%\n"
for key in sorted(combdic):
	print ''
	printdic = combdic[key]
	for x in range(1, max(combdic[key])):
		average_G = (float(printdic[x][2])+float(printdic[x][7]))/2
		std_dev_G = round(math.sqrt(((math.pow(float(printdic[x][2])-average_G, 2))+math.pow(float(printdic[x][7])-average_G, 2))/2), 8)
		average_A = (float(printdic[x][3])+float(printdic[x][8]))/2
		std_dev_A = round(math.sqrt(((math.pow(float(printdic[x][3])-average_A, 2))+math.pow(float(printdic[x][8])-average_A, 2))/2), 8)
		average_T = (float(printdic[x][4])+float(printdic[x][9]))/2
		std_dev_T = round(math.sqrt(((math.pow(float(printdic[x][4])-average_T, 2))+math.pow(float(printdic[x][9])-average_T, 2))/2), 8)
		average_C = (float(printdic[x][5])+float(printdic[x][10]))/2
		std_dev_C = round(math.sqrt(((math.pow(float(printdic[x][5])-average_C, 2))+math.pow(float(printdic[x][10])-average_C, 2))/2), 8)
		if average_G + average_A + average_T + average_C < 2:
			print " ".join([str(key), str(x), printdic[x][0], str(printdic[x][1]), str(printdic[x][6]), str(round(float(average_G) ,8)), str(round(float(average_A) ,8)), str(round(float(average_T) ,8)), str(round(float(average_C),8)), str(std_dev_G) ,str(std_dev_A) ,str(std_dev_T) , str(std_dev_C)])
		else:
			print " ".join([str(key), str(x), printdic[x][0], str(printdic[x][1]), str(printdic[x][6]), str(round(float(average_G) ,8)), str(round(float(average_A) ,8)), str(round(float(average_T) ,8)), str(round(float(average_C),8)), str(std_dev_G) ,str(std_dev_A) ,str(std_dev_T) , str(std_dev_C) , str(average_G + average_A + average_T + average_C)])

