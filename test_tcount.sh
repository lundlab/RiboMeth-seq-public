# set the variables ############################################################
cd /home/disat/data/PROJECT-tRNA-RMS
cwd=$(pwd)
# set the experiment name and barcodes
expname="tRNA_RMS_293Twt"
barcode1="ACAATG"
barcode2="CAAGAG"
barcode3="GGACTT"
fastqfile="R_2019_06_27_11_44_21_user_proton1-241-Disa_run_4_Auto_user_proton1-241-Disa_run_4_338.fastq"

# set the ref genome sequence and raw data files
dataDir="/home/disat/data/raw_Data/RMS_fastq"
genomeDir="/home/disat/data/ref_genomes/"
refgenome="hg38.tRNAscan_mature_unique"
seqs_to_perform_RMS="seqs_to_perform_tRNA_RMS.txt"

#### these are more or less standard for each project tree
workDir="${cwd}/Analysis"

scriptDir="${cwd}/Scripts"
resultDir="${cwd}/Results"

##################################################################### end variabl ### Go to workDir for Analysis
cd ${workDir} # go do "Analysis" working dir
mkdir ${expname} # make the expname dir
cp ${scriptDir}/pipeline.sh ${expname}/pipeline.${expname}.sh # copy the pipeline with all the correct variables

##### START ANALYSIS
# sort and separate reads based on the barcode
date +"%d %b-%y %T ...... sortNtrim "
mkdir trimmed
for var in ${!barcode@}; do
python ${scriptDir}/sortNtrim.py ${dataDir}/${fastqfile} ${!var} > ${expname}/trimmed/${!var}.data.BC.fq
done

# remove adapters
date +"%d %b-%y %T ...... cutadapt "
for n in $(ls ${expname}/trimmed/*BC.fq); do
cutadapt -a ATCACCGAC -m 15 --discard-untrimmed ${n} > ${n}.CA_disc.fq 2>> ${expname}/trimmed/log.cutadapt.${expname}.txt
done

# bowtie2 mapping
date +"%d %b-%y %T ...... bowtie2 "

for n in $(ls ${expname}/trimmed/*CA_disc.fq); do
cd ${genomeDir}/${refgenome}/
bowtie2 -k 10 --threads 18 -x index/${refgenome} -U ${workDir}/${n} -S ${workDir}/${n}.sam 2>> ${workDir}/${expname}/log.bowtie2.${expname}.txt
done
cd ${workDir}
mv ${expname}/trimmed/*.sam ${expname}/
# PYTHON SCRIPTS multimap + readcount + seqnumbering + SAMTOOLS mileup + pilecount + map%
date +"%d %b-%y %T ...... calculating RMS scores and SNP analysis"
for n in $(ls ${expname}/*.sam); do
#remove multimappers (Ulf's script)
python ${scriptDir}/remove_multiple_map_hits.py ${n} > ${n}.best_map.sam
# count read ends
python ${scriptDir}/readcount_5and3.py ${n}.best_map.sam ${cwd}/${seqs_to_perform_RMS} > ${n}.best_map.sam.count
#count the RMS scores
python ${scriptDir}/ms_scores.py ${n}.best_map.sam.count > ${n}.best_map.sam.count.scores
# seq numbering
python ${scriptDir}/seq_numbering.py ${genomeDir}/${refgenome}/${refgenome}.fa ${n}.best_map.sam.count.scores > ${n}.best_map.sam.count.scores.seq
# sam to sorted bam files
samtools view -u -bS ${n}.best_map.sam | samtools sort -o ${n}.best_map.sam.sort.bam
# mileup for SNP analysis
samtools mpileup -d 10000000 -f ${genomeDir}/${refgenome}/${refgenome}.fa ${n}.best_map.sam.sort.bam > ${n}.best_map.sam.sort.bam.sort.pileup
# pilecpunt for SNP analysis
python ${scriptDir}/pilecount_v5.py ${n}.best_map.sam.sort.bam.sort.pileup ${cwd}/${seqs_to_perform_RMS} > ${n}.best_map.sam.sort.bam.sort.pileup.snp
# get mapping percentages
python ${scriptDir}/map_percent.py ${n} >> ${expname}/map_percent.${expname}.txt
done


# Combining replicates
mkdir ${resultDir}/${expname}
date +"%d %b-%y %T ...... running comb_RMS.py"
replicates=$(echo $(ls ${expname}/*.seq))
python ${scriptDir}/comb_RMS.py ${replicates}  > ${resultDir}/${expname}/${expname}_RMS_comb.txt

date +"%d %b-%y %T ...... running comb_SNP.py"
replicates=$(echo $(ls ${expname}/*.snp))
python ${scriptDir}/comb_SNP.py ${replicates}  > ${resultDir}/${expname}/${expname}_SNP_comb.txt

date +"%d %b-%y %T ...... running transcript_count.py"
replicates=$(echo $(ls ${expname}/*.best_map.sam))
python ${scriptDir}/transcript_count.py ${replicates} ${genomeDir}/${refgenome}/${refgenome}.fa > ${resultDir}/${expname}/${expname}_expressed.txt

# making excel files in results Dir
cd ${resultDir}/${expname}
date +"%d %b-%y %T ...... converting to xslx"
python ${scriptDir}/txt2xlsx_RMS.py ${expname}_RMS_comb.txt
python ${scriptDir}/txt2xlsx_SNP.py ${expname}_SNP_comb.txt
python ${scriptDir}/txt2xlsx_expressed.py ${expname}_expressed.txt

date +"%d %b-%y %T ...... Cleaning up"
cd ${workDir}/${expname}
rm *.seq
rm *.scores
rm *.pileup
rm *.snp
rm *.best_map.sam
rm trimmed/*.BC.fq
rm *.bam
mkdir countfiles
mv *.count countfiles/
mkdir samfiles
mv *.sam samfiles/
date +"%d %b-%y %T ...... end script"

### can do this if possible
#date +"%d %b-%y %T ...... Running R script"
#nice Rscript Rscript_for_RMS_pipeline.R "expname"



