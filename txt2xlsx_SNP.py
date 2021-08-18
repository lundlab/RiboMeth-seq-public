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
	lineel=line.split()
	col=0
	for word in lineel:
		try:
			worksheet.write(row, col, float(lineel[col]))
		except:
			try:
				worksheet.write(row, col, int(lineel[col]))
			except:
				worksheet.write(row, col, lineel[col])
		col+=1
	row += 1
	

workbook.close()
