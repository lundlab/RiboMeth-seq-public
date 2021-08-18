#!/usr/bin/python
from sys import argv
import sys

fpileup = open(argv[1], 'r')
fseqs = open(argv[2], 'r')

my_snp_out = {}
for line in fseqs:
	lineel = line.split()
	my_snp_out[lineel[0]] = my_snp_out.get(lineel[0], {})
		
	for x in range(1, int(lineel[1])+2):
		my_snp_out[lineel[0]][x] = ['No_cov', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
print "Chromosome	position	reference_seq	Total_coverage	Reference G's	A's	U's	C's	G%	A%	U%	C%	G-insertions	A-insertions	U-insertions	C-insertions	G-deletions	A-deletions	U-deletions	C-deletions	3'RNA_lig	5'RNA_lig"
for line in fpileup:
	new=0
	ins=0
	dele=0
	three=0
	five=0
	ref=0
	tdi=0
	tdd=0
	A=0
	T=0
	G=0
	C=0
	insA=0
	insT=0
	insG=0
	insC=0
	deleA=0
	deleT=0
	deleG=0
	deleC=0
	nucl=''
	lineel = line.split()
	chrom=lineel[0] 
	num = int(lineel[1])
	refnuc=lineel[2]
	cover=lineel[3]
	if len(lineel)>5:
		nucl=lineel[4]
		qual=lineel[5]
	
	if chrom in my_snp_out:
	
		x=0
		i = 0	
		while  i < len(nucl):
			if new == 2:
				new = 1
			if new == 3:
				new = 2
			pos = nucl[i:i+1]
			if pos == '+':
				ins = 1
			if pos == '-':
				dele = 1
			if pos == '^':
				new=3
			if pos in ['.',',','G','A','T','C', 'g','a','t','c'] and dele == 0 and ins == 0 and new < 2:
				try:
					qscore = ord(qual[x:x+1])-33
				except TypeError:
					sys.stderr.write(line)
				x+=1
			if pos in ['.',','] and new == 0 and qscore >=0:
				ref = ref+1
			if pos in ['.',','] and new == 1 and qscore >=0:
				three = three+1
				ref = ref+1
				new=0
			if pos == '$' and new == 0:
				five = five+1
			if pos in ['a', 'A'] and ins == 0 and dele == 0 and new == 0  and qscore >=0:
				A = A+1
			if pos in ['t', 'T'] and ins == 0 and dele == 0 and new == 0 and qscore >=0:
				T = T+1
			if pos in ['g', 'G'] and ins == 0 and dele == 0 and new == 0 and qscore >=0:
				G = G+1
			if pos in ['c', 'C'] and ins == 0 and dele == 0 and new == 0 and qscore >=0:
				C = C+1
			if pos in ['a', 'A'] and new ==1 and qscore >=0:
				A = A+1
				three = three+1
				new=0
			if pos in ['t', 'T']  and new ==1 and qscore >=0:
				T = T+1
				three = three+1
				new=0
			if pos in ['g', 'G']  and new ==1 and qscore >=0:
				G = G+1
				three = three+1
				new=0
			if pos in ['c', 'C']  and new ==1 and qscore >=0:
				C = C+1
				three = three+1
				new=0
			if  tdi == 1 and pos in numbers:
				ins =int(pos)+10
				tdi=0
			if tdi == 1 and pos not in numbers:
				tdi = 0
			if ins == 1 and pos in numbers:
				ins = int(pos)
				tdi = 1
			if ins >= 1 and pos in ['a', 'A']:
				insA=insA+1
				ins=ins-1
			if ins >= 1 and pos in ['t', 'T']:
				insT=insT+1
				ins=ins-1
			if ins >= 1 and pos in ['g', 'G']:
				insG=insG+1
				ins=ins-1
			if ins >= 1 and pos in ['c', 'C']:
				insC=insC+1
				ins=ins-1			
			if  tdd == 1 and pos in numbers:
				ins =int(pos)+10
				tdd=0
			if tdd == 1 and pos not in numbers:
				tdd = 0
			if dele == 1 and pos in numbers:
				dele = int(pos)
				tdd = 1
			if dele == 1 and pos in ['a', 'A']:
				deleA=deleA+1
				dele = dele-1
			if dele >= 1 and pos in ['t', 'T']:
				deleT=deleT+1
				dele = dele-1
			if dele >= 1 and pos in ['g', 'G']:
				deleG=deleG+1
				dele = dele-1
			if dele >= 1 and pos in ['c', 'C']:
				deleC=deleC+1
				dele = dele-1
			i+=1
		if ref+G+A+T+C != 0 and chrom in my_snp_out:
			a = 100*float(A)/(float(ref)+G+A+T+C)
			t = 100*float(T)/(float(ref)+G+A+T+C)
			g = 100*float(G)/(float(ref)+G+A+T+C)
			c = 100*float(C)/(float(ref)+G+A+T+C)
			if refnuc == 'T':
				refnuc = 'U'
			my_snp_out[chrom][num] = [refnuc, cover, ref, G, A, T, C, g, a, t, c, insG, insA, insT, insC, deleG, deleA, deleT, deleC, three, five]
		elif ref+G+A+T+C == 0 and chrom in my_snp_out:
			if refnuc == 'T':
				refnuc = 'U'
			my_snp_out[chrom][num] = [refnuc, cover, ref, G, A, T, C,'0','0','0','0', insG, insA, insT, insC, deleG, deleA, deleT, deleC, three, five]

for key in sorted(my_snp_out):
	for x in range(1, len(my_snp_out[key])+1):
		my_print_str=''
		for y in range(0, len(my_snp_out[key][x]) ):
			my_print_str += str(my_snp_out[key][x][y])+' '
		print key, x, my_print_str
