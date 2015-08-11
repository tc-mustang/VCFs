#!/usr/bin/env/python -u 

#   Change the reference allele from a VCF file using the reference genome
#   Depending on the file it would need some tweeks
#   rjl278@cornell.edu
#   LIST + FRequencies

import sys
import re
import os
from itertools import islice

lista = list()
chromosome = 1


while chromosome <19:

    print "solving problems on chromosome %d" %(chromosome)
    
    os.system("grep \"WARNING\" /home/roberto/Software/snpEff/chr%s/snpEff_ann.vcf | awk -F\"\t\" '{print $3}' > tmp" %(chromosome))
    VCFs = "/home/DB/M.esculenta/VCF_V6/chr%s/chr%s_filt.vcf.recode.vcf" %(chromosome, chromosome)
    
    with open("tmp") as f:
        tmp = list()
        for line in f:
            lista.append(line.rstrip())
    
    with open(VCFs) as f:
        head = list(islice(f, 11))
        
        fi = open("chr%s_correct.vcf"%(chromosome), 'w')
        
        
        for elements in head:
            fi.write(elements)
        
        for line in f:
            a = line.split()  
            if a[2] in lista:
                parta = "\t".join(a[0:3])
                os.system("extract_fasta_2.pl -c%s -b %s -e %s /home/DB/M.esculenta/V6_assembly/cassavaV6_chrAndScaffoldsCombined_numeric.fa | tail -n 1 > tmp1" %(chromosome, a[1], a[1]))
                
                #f = open("tmp1","r")
                #partb = (f.read(1))
                #partc = "\t".join(a[5:])
                #fi.write(parta+"\t"+partb+"\t"+a[3]+"\t"+partc+"\n")
                #log = partb+"\t"+a[1]+"\t"+a[2]+"\t"+a[3]+"\t"+a[4]
                #print log
                
                f = open("tmp1","r")
                partb = (f.read(1))
                partc = "\t".join(a[4:])
                fi.write(parta+"\t"+partb+"\t"+partc+"\n")
                
                log = partb+"\t"+a[1]+"\t"+a[2]+"\t"+a[3]+"\t"+a[4]
                print log
                
            #else:
            #    fi.write(line)
                
    print "Done with chromosome %d " %chromosome
    fi.close()
    os.system("rm tmp")
    os.system("rm tmp1")
    chromosome += 1

  
