# set the variables ############################################################
# set the variables ############################################################
source /opt/anaconda3/bin/activate # optional
conda activate RMS # optional

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
resultDir="${cwd}/results"


cd ${workDir}/${expname}

### can do this if possible
date +"%d %b-%y %T ...... Running R script"
mkdir R_plots
# run QC script in R: arguments are: "expname" "path_to_RMA.anno" "path_to_output"
nice Rscript ${scriptDir}/Rscript_QC_for_RMS_pipeline.R ${expname} ${scriptDir}/helpfiles ${resultDir}/${expname}/R_plots

conda deactivate
conda deactivate

