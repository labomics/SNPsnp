# SNPsnp
## Overview
This model is aimed at providing guidance for researchers to determine the optimal and affordable sequencing depth for their projects. 

SNPsnp (SNP saturation number prediction) can predict the saturated SNP number of a strain, given its sequencing coverage, sequencing depth, abundance, genome length, SNP number and SNP density. A test sample could be sequenced in affordable depth first to determine if more data is needed. 

## Requirements
* python (3.7)
* pandas 
* numpy
* sklearn
* sys

## Usage
When you want to predict the saturated SNP number of a strain, you can use this model. The usage of this model is extremely easy. All you need is a file that consisting of sequencing coverage, sequencing depth, abundance, genome length, SNP number and SNP density at the current sequencing depth. Then you can get the predicted SNP saturation number to judge whether your current sequencing depth is suifficent for your research. 

```
python useSNPsnp.py [inputfile]
```

## Example
The output file consists of eight columns. The first seven colums are your input data and the last column is the predicted SNP saturation number of the corresponding strain. As shown in example folder, the predictSNPs.txt is the output.

```
python useSNPsnp.py example/test.txt
```
