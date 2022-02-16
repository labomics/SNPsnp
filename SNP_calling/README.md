# metagenomic_SNP_calling
## Overview
This framework contains quality control, construction of microbial reference genomes, SNP calling, selection of strains and depth filteration threshold for strains. 

### Quality control of reads

FastQC (http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) was used to have an overview of raw data. After having a general understanding of quality, we implemented personalized quality control strategies by combining Trimmomatic with python programs in step1_qc/trimmomatic.py. Then quality control used the following criteria: (1) adaptors were removed; (2) low-quality bases (<Q20) were trimmed; (3) reads containing less than 45 bases were removed. Parameters are ‘TRAILING:20 SLIDING- WINDOW:5:10 MINLEN:45 AVGQUAL:20’. (4) sites whose base call number (f) was beyond f ± 2 × SD (standard deviation) were cut. 

### Construction of microbial reference genome

With a large number of microbial reference genomes already in hand, it would cost vast computing resources and considerable time if we integrate all microbial reference genomes available as our reference genome. Only strains detected in samples were reserved as the final reference genome. MetaPhlAn2 was used to profile the microorganisms (see step2/metaphlan.py). The final reference genomes achieved by steps in folder step3_getRef are used in subsequent analysis.

### SNP calling 
According to the research of Altmann et al (A beginners guide to SNP calling from high-throughput DNA-sequencing data. Hum Genet 2012; 131:1541–54.), the SNP calling results using SAMTools have around 85 percent in common with that using GATK. Taking accuracy and run time into account, SAMTools was chosen as one of the softwares calling SNPs. The alignment of duplicates by BWA was first marked and filtered by Picard (http://broadinstitute.github.io/picard/). Then SAMTools was used to call SNPs with parameters ‘- vmO z -V indels’ and the results were filtered by VCFTools with parameters ‘+/d=10/a=4/Q=15/q=10/’. VarScan2 is very robust in adjusting thresholds such as coverage and minimum allele frequency, which makes it advantageous for the detection of low-allele-frequency variants in high-depth datasets. To reduce SNP false positives, VarScan2 was also used to call SNPs with ‘-min-coverage 10 -min-reads2 4 -min-var-freq 0.2 -p-value 0.05’. SNPs detected by both SAMTools and VarScan2 were selected for the next step of analysis as tentative SNPs.(see details in step4_callSNP).

### Selection of strains
Burrows-Wheeler Aligner-maximal exact match (BWA-MEM) was chosen to align clean reads to the constructed microbial reference genome in default settings. Given multiple alignment problem, we retained only the unique matched reads to increase the accuracy of subsequent variant calling. While large quantities of strains exist in gut microbiome, lots of them are with low abundance. Hence, we chose dominant strains (relative abundance over 1%) for further analysis. 

### Depth filteration threshold for strains
When the sequencing size of samples is not normal, it is difficult to determine a reasonable filter threshold, especially for sequencing depth. In order to avoid the biases by subjectively determining the sequencing depth filteration threshold, we determined the depth filteration threshold for strains by fitting the base depth distribution of each strain.

## Pre-requisites
This part requires FastQC, Trimmomatic, MetaPhlAn2.0, bowtie2, bwa, Samtools, picard, bcftools, VarScan2, vcftools installed. 

## Flowchart
<img src="flowchart.png" width = "600" height = "400" alt="" align=center />

### Usage Examples

To help better understand how this framework works, we use data in filefolder test to run this framwork. It should be noted that due to the large amount of data in researches and our small test data, the threshold standard is slightly different.

Considering reseaches often includes large samples, we suggest that a file contains sample names is needed, which is list1.txt here.

step1_qc performs quality control with a file contains sample name, datadir and outdir needed. The input is raw data and the output is clean data in test/clean_data.

    python step1_qc/trimmomatic.py filepath/filename datadir outdir                             `

step2_metaphlan profiles the microorganisms and their relative abundances in each sample. The input is clean data and the output is the info of microorganisms and their relative abundances in test/metaphlan2. 

    python step2_metaphlan/metaphlan.py metaphlan_dir out_dir  fastq_dir 

step3_getRef constructs microbial reference genome by selecting strains that meet certain conditions. Then you need to download reference genome from NCBI according to GCFid and build index for Reffna. You can see details in test/ref.  

    python2 step1_stat.py test/metaphlan2 > species.txt  
    python2 step2_getStrain.py test/metaphlan2 > mappedstrain.txt   
    python2 step3_getrefid.py > mappedGCF.txt   
    
step4_callSNP includes calling SNPs by Samtools and VarScan2 respectively and some filter processes. The results of snp calling by samtools are in test/callSNP/output and test/callSNP/savedBams. The results by VarScan2 are in test/callSNP/voutput.

    python step1_callSNP.py 1
    python step2_varscan.py 1
    python step3_filtervcf.py 1
    python step4_gen_newvcf.py 1

    
