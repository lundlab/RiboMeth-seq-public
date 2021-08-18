#!/usr/bin/python
from sys import argv

fin = open(argv[1], "r")

import math

mapdic = {}
averagedic = {}
vfivedic = {}
methpercentdic = {}

jscoredic={}
total=0

for line in fin:
	lineel = line.split()
	if len(lineel) >1:
		mapdic[lineel[0]] = mapdic.get(lineel[0], {})
		mapdic[lineel[0]][int(lineel[1])] = int(lineel[2]),int(lineel[3]),int(lineel[4])
		total+=int(lineel[4])

for key in mapdic:
	one=two=thr=fou=fiv=six=sev=eig=nin=ten=ele=twe=thi=0
	b=mapdic[key]
	for x in range(1, int(max(mapdic[key])+1)):
		one=two
		two=thr
		thr=fou
		fou=fiv
		fiv=six
		six=sev
		sev=eig
		eig=nin
		nin=ten
		ten=ele
		ele=twe
		twe=thi
		thi=float(b[x][2])
		average = float((one*0.5+two*0.6+thr*0.7+fou*0.8+fiv*0.9+six+eig+nin*0.9+ten*0.8+ele*0.7+twe*0.6+thi*0.5)/9)

		
		averagedic[key] = averagedic.get(key, {})
		averagedic[key][x] = average

		vfivedic[key] = vfivedic.get(key, {})
		vfivedic[key][x] = float(abs(sev-average)/(sev+1))

		methpercentdic[key] = methpercentdic.get(key, {})
		if sev<average:
			methpercentdic[key][x] = 1-(sev/average)
		else:
			methpercentdic[key][x] = 0
		
		mleft=float(one+two+thr+fou+fiv+six)/6
		mright=float(eig+nin+ten+ele+twe+thi)/6
		sdleft=  math.sqrt((math.pow(float(one)-mleft, 2)+math.pow(float(two)-mleft, 2)+math.pow(float(thr)-mleft, 2)+math.pow(float(fou)-mleft, 2)+math.pow(float(fiv)-mleft, 2)+math.pow(float(six)-mleft, 2))/6)
		sdright= math.sqrt((math.pow(float(eig)-mright,2)+math.pow(float(nin)-mright,2)+math.pow(float(ten)-mright,2)+math.pow(float(ele)-mright,2)+math.pow(float(twe)-mright,2)+math.pow(float(thi)-mright,2))/6)
		jscore = 1-((2*sev+1)/(0.5*abs(mleft-sdleft)+sev+0.5*abs(mright-sdright)+1))
		jscoredic[key] = jscoredic.get(key, {})
		if jscore > 0:
			jscoredic[key][x] = jscore
		else:
			jscoredic[key][x] = 0


print '''RNA Position Nucl 5'_reads 3'_reads 5'+3' Local_average v5_score v6_score Meth%'''

for key in sorted(mapdic):
	b=mapdic[key]
	for x in range(1, int(max(mapdic[key])+1)):
		try:
		#	if averagedic[key][x+6]:
			if x>6:
				print ' '.join([key, str(x), str(b[x][0]), str(b[x][1]), str(b[x][2]), str(vfivedic[key][x+6]), str(jscoredic[key][x+6]), str(methpercentdic[key][x+6]) ] )
			else:
				print key, x, b[x][0], b[x][1], b[x][2], 0, 0, 0
		except KeyError:
			print key, x, b[x][0], b[x][1], b[x][2], 0, 0, 0
