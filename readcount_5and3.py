#!/usr/bin/python
from sys import argv
fsam = open(argv[1], "r") #fsam is the sequence alignment map
fsequences = open(argv[2], "r") #fsequences should contain a list of sequences for which RMS count will be calculated



class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

three = AutoVivification()
five = AutoVivification()
my_dic_ranges={}
direction=['16','272'] #16 and 272 represents reverse complimentary mapping in the SAM-file. This corresponds to mapping to transcripts and may need to be extended if genomic reference is used for mapping reads
my_seqs=[]
for line in fsequences: #reads in the sequences in the fsequences file and stores these in my_seqs
	fa_lineel = line.split()
	my_seqs.append(fa_lineel[0])

define_dics=0

import re
for line in fsam:
	lineel=line.split()
	editdist=0
	
	#identifies the header line for each sequence in
	#the reference library if present in the sequence file
	if lineel[1].split(':')[0] == 'SN' and lineel[1].split(':')[1] in my_seqs:
		my_dic_ranges[lineel[1][3:]]=lineel[2][3:]
		define_dics=0
		
	if lineel[1] in direction and lineel[2] in my_seqs:
		if define_dics==0:
			for key in my_dic_ranges:
				for x in range(0, int(my_dic_ranges[key])+1):
					five[key][x]=0
					three[key][x]=0
			define_dics=1
		cigar = re.split('\M|\I|\D',lineel[5]) # determines if there's indels in 5' (read)end


		my_subs = line.split('MD:Z:')[1].split()[0]
		subdistance = re.split('\G|A|\T|\C|\^', my_subs) # determines if there's substitution in the read
		
		if int(cigar[0]) > 3 and subdistance[0] > 3:
			try:
				five[lineel[2]][int(lineel[3])-1] += 1 
			except TypeError:
				print line.rstrip()

		
		editdist = 0 # Calculates the actual 3'end taking indels into account
		if 'I' in lineel[5]:
			inserts = re.split('\I',lineel[5])
			y=0
			while y < len(inserts)-1:
				my_ins = re.split('\M|\D',inserts[y])
				editdist -= int(my_ins[-1])
				y +=1

		if 'D' in lineel[5]:
			deletions = re.split('D',lineel[5])
			y=0
			while y < len(deletions)-1:
				my_del = re.split('\M|\I',deletions[y])
				editdist += int(my_del[-1])
				y +=1

		if int(cigar[-2]) > 3 and subdistance[-1] > 3:
			readlength = len(lineel[9]) + editdist-1
			
			three[lineel[2]][int(lineel[3])+readlength] += 1 

for key in sorted(my_dic_ranges): #prints read-end counts for sequences specified in argv2
	if key in my_seqs:
		for x in range(1, int(my_dic_ranges[key])+1):
			print key, x, five[key][x], three[key][x], five[key][x]+three[key][x]

