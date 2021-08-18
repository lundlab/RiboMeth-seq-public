# set the variables ############################################################
# set the variables ############################################################
source /opt/anaconda3/bin/activate # optional
conda activate ribomethseq # optional

cd /home/disat/data/PROJECT-rRNA-RMS
cwd=$(pwd)
# set the experiment name and barcodes
expname="pipe_test"
barcode1="ACAATG"
barcode2="CAAGAG"
barcode3="GGACTT"
#fastqfile="R_2019_06_27_11_44_21_user_proton1-241-Disa_run_4_Auto_user_proton1-241-Disa_run_4_338.fastq"
fastqfile="RMS.test.fastq"
# set the ref genome sequence and raw data files

#dataDir="/home/disat/data/raw_Data/RMS_fastq"
dataDir="/home/disat/data/PROJECT-rRNA-RMS/raw_data"
genomeDir="/home/disat/data/ref_genomes/"
refgenome="hsa_sno+sn+rRNA" # put the basename here i.e leave out ".fa"
path_to_cutadapt2_6="/home/disat/.local/bin" # I need this since I had to install cutadapt 2.6 in my local bing

#### these are more or less standard for each project tree
workDir="${cwd}/analysis"
scriptDir="${cwd}/scripts"
cd ${workDir}
mkdir ${expname}  # make the expname dir
mkdir ${expname}/results
resultDir="${workDir}/${expname}/results"

##################################################################### end variables

cp ${scriptDir}/pipeline.sh ${expname}/pipeline.${expname}.sh # copy the pipeline with all the correct variables

##### START ANALYSIS
# sort and separate reads based on the barcode
date +"%d %b-%y %T ...... sortNtrim "
mkdir ${expname}/trimmed
for var in ${!barcode@}; do
python ${scriptDir}/sortNtrim.py ${dataDir}/${fastqfile} ${!var} > ${expname}/trimmed/${!var}.data.BC.fq
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
date +"%d %b-%y %T ...... running comb_RMS.py"
replicates=$(echo $(ls ${expname}/*.seq))
python ${scriptDir}/comb_RMS.py ${replicates}  > ${resultDir}/${expname}_RMS_comb.txt

date +"%d %b-%y %T ...... running comb_SNP.py"
replicates=$(echo $(ls ${expname}/*.snp))
python ${scriptDir}/comb_SNP.py ${replicates}  > ${resultDir}/${expname}_SNP_comb.txt

date +"%d %b-%y %T ...... running transcript_count.py"
replicates=$(echo $(ls ${expname}/*.best_map.sam))
python ${scriptDir}/transcript_count.py ${replicates} ${genomeDir}/${refgenome}/${refgenome}.fa > ${resultDir}/${expname}_expressed.txt

# making excel files in results Dir
cd ${resultDir}
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
mv ../seqs_to_perform_RMS.txt seqs_to_perform_RMS.txt
date +"%d %b-%y %T ...... end script"

### can do this if possible
date +"%d %b-%y %T ...... Running R script"
# run QC script in R: arguments are: "expname" "path_to_RMS.anno" "path_to_output"
nice Rscript ${scriptDir}/Rscript_QC_for_RMS_pipeline.R ${expname} ${scriptDir}/helpfiles ${resultDir}

conda deactivate
conda deactivate

