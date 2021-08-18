# RiboMeth-seq rRNA analysis

RiboMeth-seq analysis from IonTorrent RNA seq data, counting read ends and calculating RiboMeth-seq score
transcrip_count.py has been changed from Ulf's original script to include real RPKM calculations
still need to change the SNP_ and RMS_comb to actually print out the barcodes in the header since this does not work now


## Getting Started

1) Cerate an index for bowtie2 from the .fa ref_seq
2) To run the whole pipeline setup all environment variables including used barcodes and paths in the beginning of the pipeline.sh

### Prerequisites

This pipeline needs:
python version 2.7
cutadapt 2.6 = enables multicore running!!! (optional)
bowtie2 version?


```
Give examples
```

### Installing

This tutorial is for working in a conda anv but obviously this is optional

```

pip3 install --user cutadapt # installs cutadapt 2.6 = enables multicore running!!! NB installation has to be donw with python 3.6 so do it before changing to 2.7
Create conda env as follows
source /opt/anaconda3/bin/activate # optional
conda create --name RMS python=2.7 # create an env called RibOxi which will run python 2.7
conda activate RMS
conda install -c anaconda xlsxwriter # in the env you can install the htslib with bioconda
pip install statistics # use for stdev in python script transcrip_count.py
conda deactivate
```

R packages

```
install.packages("openxlsx")
install.packages("PRROC")
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
 cd ${path_to_ref_seq}
 mkdir index
 bowtie2-build hsa_sno+sn+rRNA.fa index/hsa_sno+sn+rRNA
 samtools faidx hsa_sno+sn+rRNA.fa

```

### And coding style tests

Explain what these tests test and why

```
Give an example
```


## Authors

* **Disa Tehler** - *Initial work*



## Acknowledgments

* Ulf Birkedal for creating all the original python scripts

