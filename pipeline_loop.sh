# set the variables ############################################################
source /opt/anaconda3/bin/activate
conda activate trna
cwd="/home/disat/data/PROJECT-tRNA-RMS" # set the root dir
#### these are more or less standard for each project tree
workDir="${cwd}/analysis"
scriptDir="${cwd}/scripts"
resultDir="${cwd}/results"

# set the ref genome sequence and raw data files
dataDir="/home/disat/data/raw_Data/RMS_fastq/loop"
genomeDir="/home/disat/data/ref_genomes/"
refgenome="hsa_tRNA_TpsiCdb_N" # put the basename here i.e leave out ".fa"

### set expname basted on folder name in dataDir
# this line finds all dirs in dataDir - each will contain a .fq file and one or more variable.txt files named after the experiment
for fqdir in $(ls ${dataDir}/); do
fqfile=$(ls ${dataDir}/${fqdir}/*.fastq)
# for each dir in dataDir (corresponding to the fq files per chip) read in the expname from the filename
for exp in $(ls ${dataDir}/${fqdir}/*.txt); do
export $(grep -v "^#" ${exp} | xargs)
expname=${tissue_of_origin}-${experiment_name}_name${person_who_made_library}
date +"%d %b-%y %T ...... Starting with experiment ${expname}"
echo "..........................Using barcodes:"
echo ".......................... ${barcode1}"
echo ".......................... ${barcode2}"
echo ".......................... ${barcode3}"
echo "..........................Fastqfile: ${fqfile}"
echo "..........................Refgenome: ${refgenome}"

##################################################################### end variables
### Go to workDir for Analysis
cd ${workDir} # go do "Analysis" working dir
mkdir ${expname} # make the expname dir
cp ${scriptDir}/pipeline.sh ${expname}/pipeline.${expname}.sh # copy the pipeline with all the correct variables


##### START ANALYSIS
# sort and separate reads based on the barcode
date +"%d %b-%y %T ...... sortNtrim "
mkdir ${expname}/trimmed
for var in ${!barcode@}; do
python ${scriptDir}/sortNtrim.py ${fqfile} ${!var} > ${expname}/trimmed/${!var}.data.BC.fq
done

# remove adapters
date +"%d %b-%y %T ...... cutadapt "
for n in $(ls ${expname}/trimmed/*BC.fq); do
/home/disat/.local/bin/cutadapt -a ATCACCGAC -m 15 -j 18 --discard-untrimmed ${n} > ${n}.CA_disc.fq 2>> ${expname}/trimmed/log.cutadapt.${expname}.txt
done

# bowtie2 mapping
date +"%d %b-%y %T ...... bowtie2 "
mkdir ${expname}/bamfiles # make this dir to put sam to bam files later for saving
for n in $(ls ${expname}/trimmed/*CA_disc.fq); do
mfile=${n##*/}
cd ${genomeDir}/${refgenome}/
bowtie2 -k 10 --threads 18 -x index/${refgenome} -U ${workDir}/${n} -S ${workDir}/${expname}/${mfile}.sam 2>> ${workDir}/${expname}/bamfiles/log.bowtie2.${expname}.txt
done

cd ${workDir}
## PYTHON SCRIPTS multimap + readcount + seqnumbering + SAMTOOLS mileup + pilecount + map%
date +"%d %b-%y %T ...... calculating RMS scores and SNP analysis"
for n in $(ls ${expname}/*.sam); do
cp ${genomeDir}/${refgenome}/${refgenome}.fa.fai seqs_to_perform_RMS.txt
#remove multimappers (Ulf's script)
python ${scriptDir}/remove_multiple_map_hits.py ${n} > ${n}.best_map.sam
# count read ends
python ${scriptDir}/readcount_5and3.py ${n}.best_map.sam seqs_to_perform_RMS.txt > ${n}.best_map.sam.count
#count the RMS scores
python ${scriptDir}/ms_scores.py ${n}.best_map.sam.count > ${n}.best_map.sam.count.scores
# seq numbering
python ${scriptDir}/seq_numbering.py ${genomeDir}/${refgenome}/${refgenome}.fa ${n}.best_map.sam.count.scores > ${n}.best_map.sam.count.scores.seq
# sam to sorted bam files
samtools view -u -bS ${n}.best_map.sam | samtools sort -o ${n}.best_map.sam.sort.bam
# mileup for SNP analysis
samtools mpileup -d 10000000 -f ${genomeDir}/${refgenome}/${refgenome}.fa ${n}.best_map.sam.sort.bam > ${n}.best_map.sam.sort.bam.sort.pileup
# pilecpunt for SNP analysis
python ${scriptDir}/pilecount_v5.py ${n}.best_map.sam.sort.bam.sort.pileup seqs_to_perform_RMS.txt > ${n}.best_map.sam.sort.bam.sort.pileup.snp
# get mapping percentages
python ${scriptDir}/map_percent.py ${n} >> ${expname}/bamfiles/map_percent.${expname}.txt
# sam to sorted bam files
samtools view -u -bS ${n} | samtools sort -o ${n%.sam}.sorted.bam
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
mkdir countfiles
rm trimmed/*.BC.fq
rm *.best_map.sam.sort.bam
rm *.seq
rm *.scores
rm *.pileup
rm *.snp
rm *.sam
mv *.bam bamfiles/
mv *.count countfiles/
date +"%d %b-%y %T ...... end script"

## can do this if possible
#date +"%d %b-%y %T ...... Running R script"
#nice Rscript Rscript_for_RMS_pipeline.R "expname"

done # done with expname in first .txt file
done # done with fqDir

conda deactivate
conda deactivate
