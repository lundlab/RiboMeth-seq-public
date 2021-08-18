#!/usr/bin/python
from sys import argv
import math



frmsone = open(argv[1], "r")
frmstwo = open(argv[2], "r")
print 'Data_handling_v3   '+argv[1].split('/')[-2]+'      '+argv[2].split('/')[-2]
print "Subunit Position Nucleotide 5'_reads 3'_reads 5'+3' v5_score v6_score Meth% 5'_reads 3'_reads 5'+3' v5_score v6_score Meth% Av.Meth% Std.dev. >=0.75"

my_combdic = {}

for line in frmsone:
	lineel = line.split()
	try:
		my_combdic[lineel[0]] = my_combdic.get(lineel[0], {})
		my_combdic[lineel[0]][int(lineel[1])] = lineel[2], int(lineel[3]), int(lineel[4]), int(lineel[5]), float(lineel[6]), float(lineel[7]), float(lineel[8])
	except ValueError:
		pass

for line in frmstwo:
	lineel = line.split()
	try:
		my_combdic[lineel[0]][int(lineel[1])] += int(lineel[3]), int(lineel[4]), int(lineel[5]), float(lineel[6]), float(lineel[7]), float(lineel[8])
	except ValueError:
		pass
	except KeyError:
		print line.rstrip() , '!!!!!'


for my_keyone in sorted(my_combdic):
	my_printdic = my_combdic[my_keyone]
	print ''
	for my_keytwo in my_printdic:
		my_printlist = []
		try:
			rms_average = (my_printdic[my_keytwo][6]+my_printdic[my_keytwo][12])/2
			std_dev = math.sqrt ((math.pow(my_printdic[my_keytwo][6]-rms_average , 2)+math.pow(my_printdic[my_keytwo][12]-rms_average , 2))/2)
		except IndexError:
			print my_printdic[my_keytwo]
		for i in range(0, len( my_printdic[my_keytwo] )):
			my_printlist.extend( [str(my_printdic[my_keytwo][i]) ])
		if rms_average >= 0.75:
			print my_keyone, my_keytwo, ' '.join(my_printlist), rms_average, std_dev, '1'
		else:
			print my_keyone, my_keytwo, ' '.join(my_printlist), rms_average, std_dev


