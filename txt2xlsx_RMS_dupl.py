#!/usr/bin/python
from sys import argv
fin = open(argv[1], "r")

import xlsxwriter

workbook = xlsxwriter.Workbook(argv[1]+'.xlsx')
worksheet = workbook.add_worksheet()

worksheet.freeze_panes(2, 0)

row = 0
col = 0

for line in fin:
	lineel=line.split()
	col=0
	try:
		if len(lineel) >=16:
			for word in lineel:
				try:
					worksheet.write(row, col, int(lineel[col]))
				except:
					try:
						worksheet.write(row, col, float(lineel[col]))
					except:
						worksheet.write(row, col, lineel[col])
				col+=1
		elif len(lineel) == 0:
			worksheet.write(0, 0, '')
		else:
				worksheet.write(0, 0, lineel[0])
				worksheet.write(0, 3, lineel[1])
				worksheet.write(0, 9, lineel[2])
				worksheet.write(0, 15, 'Average')

	except IndexError:
		print 'Error with line:', line.rstrip()
			
	row += 1
	

workbook.close()
