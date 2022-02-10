#!/usr/bin/python
import re
import sys
import gzip
import os

with open("strains.txt",'r') as inpf1:
    for line1 in inpf1:
        line1 = line1.strip()
        gfile = "%s.genomeInfo.txt"%line1
        contigs = set()
        with open(gfile,'r') as inpf2:
            for line2 in inpf2:
                line2 = line2.strip()
                tarray = line2.split("\t")
                contig = tarray[0]
                contigs.add(contig)
        outfile = "./%s.vcf"%(line1)
        vcffile = "sample.vcf.gz"
        with open(outfile,'w') as outpf:
            with gzip.open(vcffile,'r') as inpf:
                for line in inpf:
                    line = line.strip()
                    if re.match("#",line):
                        continue
                    array = line.split("\t")
                    contig1 = array[0]
                    if contig1 in contigs:
                        outpf.write("%s\n"%line)

dfile = "./subdepth.txt"
with open(dfile,'r') as inpf:
    for line in inpf:
        line = line.strip()
        genome = line.split("\t")[0]
        depth = line.split("\t")[1]
        vfile = "%s.final.vcf"%(genome)
        sfile = "./%s.vcf"%(genome)
        with open(vfile,'w') as outpf:
            with open(sfile,'r') as inpf2:
                for line2 in inpf2:
                    line2 = line2.strip()
                    tarray = line2.split("\t")
                    dep = float(tarray[7].split(";")[0].split("=")[1])
                    if dep < float(depth):
                        continue
                    outpf.write("%s\n"%line2)



