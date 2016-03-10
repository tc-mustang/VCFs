#!/usr/bin/env python

# This script will correct the problem of the "multiple alleles"
# when the REF allele is not present in our population
# Any questions to Roberto Lozano: rjl278@cornell.edu
# 

import sys
import re
import os
import heapq
import math
from itertools import islice
import itertools
import gzip
import subprocess

## Factorial function:

def nCr(n,r):
    f = math.factorial
    return f(n)/f(r)/f(n-r)

## Open the files

vcf = sys.argv[1];
out = sys.argv[2];

missing = re.compile("./.:0,0,0:0")

with open(vcf, 'rb') as f, gzip.open(out, 'wb') as f_out:
     
    head = list(islice(f, 11))

    for elements in head:
            f_out.write(elements)
                
    for elements in f:
        a = elements.split()
        
        #If the markers are cool looking one REF, one ALT we just print the marker no filters no problems  
        if re.search("^[ATCG]$", a[4]) :
            f_out.write(elements)
        
        #If the markers are multi-allelic we have to do a sanity check
        
        #if the markers are really multi-allelic we just omit them no need to work with this guys
        elif re.search("^[ATCG],[ATCG]$", a[4]) and re.search("0/\d|\d/0", elements) :
            next
        
        #if the markers are tagged as multiallelic BUT the reference allele ("0" is never present)
        elif re.search("^[ATCG],[ATCG]$", a[4]) and not re.search("0/\d|\d/0", elements) :
            alts = a[4].split(",")
            genotypes = a[9:]
            genotypes_list_per_marker = list()
            
            for genos in genotypes:
                if missing.match(genos): 
                    genotypes_list_per_marker.append("./.:0,0:0")
                else:
                   
                    # Getting the read counts for the two alleles
                    ref = int(str(re.findall(",\d+,", genos)[0])[1])
                    alt =  int(str(re.findall(",\d+\:", genos)[0])[1])
                    
                    n = int(ref + alt)
                    o = n - alt
                    e = 0.00025
                    
                    L_AA = nCr(n,alt) * e**alt * (1-e)**(n-alt)
                    L_AB = nCr(n,alt) * 0.5**alt * 0.50**(n-alt)
                    L_BB = nCr(n,o) * (1-e)**alt * e**(o)
                
                    maximum = max(L_AA, L_AB, L_BB)
                    
                    AA = int(round( -10 * math.log10(L_AA/maximum)))
                    if AA > 255:
                        AA = 255
                    AB = int(round( -10 * math.log10(L_AB/maximum)))
                    if AB > 255:
                        AB = 255
                    BB = int(round( -10 * math.log10(L_BB/maximum)))
                    if BB > 255:
                        BB = 255
                        
                    PLn = AA, AB, BB
                    QG = heapq.nlargest(2, PLn)[1]
                    
                    PLr = str(AA), str(AB), str(BB)
                    PL = ",".join(PLr) 
                    
                    if genos[0:3] == "1/1" :
                        tmp = "0/0:" + str(ref) + "," + str(alt) + ":" + str(n) + ":" + str(QG) + ":" + PL
                        genotypes_list_per_marker.append(tmp)
                        
                    elif genos[0:3] == "2/1" or genos[0:3] == "1/2":
                        tmp = "0/1:" + str(ref) + "," + str(alt) + ":" + str(n) + ":" + str(QG) + ":" + PL
                        genotypes_list_per_marker.append(tmp)
                    
                    elif genos[0:3] == "2/2" :
                        tmp = "1/1:" + str(ref) + "," + str(alt) + ":" + str(n) + ":" + str(QG) + ":" + PL
                        genotypes_list_per_marker.append(tmp)

            #Re-arming everything:
            
            first = "\t".join(a[0:3])
            second = "\t".join(a[5:9])
            alleles = "\t".join(alts)
            genotypes = "\t".join(genotypes_list_per_marker)
            
            lista = first+"\t"+alleles+"\t"+second+"\t"+genotypes+"\n"
            f_out.write(lista)
        

