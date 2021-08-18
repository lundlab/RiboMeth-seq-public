#!/usr/bin/python
from sys import argv
fin = open(argv[1], "r")

import xlsxwriter



workbook = xlsxwriter.Workbook(argv[1]+'.xlsx')
worksheet = workbook.add_worksheet()
worksheet.freeze_panes(1, 0)
row = 0
col = 0

for line in fin:
	lineel=line.split('\t')
	col=0
	for x in range(0, len(lineel)):
		lineel[x] = lineel[x].decode("utf8")
		try:
			worksheet.write(row, col, float(lineel[x]))
		except:
			try:
				worksheet.write(row, col, int(lineel[x]))
			except:
				worksheet.write(row, col, lineel[x])
		col+=1
	row += 1
	

workbook.close()
