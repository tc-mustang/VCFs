#!/usr/bin/env python

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


while chromosome <2:

    print "solving problems on chromosome %d" %(chromosome)
    
    #os.system("grep \"WARNING\" /home/roberto/Software/snpEff/chr%s/snpEff_ann.vcf | awk -F\"\t\" '{print $3}' > tmp" %(chromosome))
    VCFs = "/home/DB/M.esculenta/VCF_V6/correct_VCF/chr%d_correct.vcf" %(chromosome)
    
    
    with open(VCFs) as f:
        head = list(islice(f, 11))
        
        fi = open("chr%s_indel.vcf"%(chromosome), 'w')
        
        for elements in head:
            fi.write(elements)
        
        for line in f:
            a = line.split()  
            if a[3] == a[4]:              
                                
                parta = a[0]+"\t"+str(int(a[1])-1)+"\t"+a[2]
                                                            
                position = int(a[1])-1
                os.system("extract_fasta_2.pl -c%s -b %d -e %s /home/DB/M.esculenta/V6_assembly/cassavaV6_chrAndScaffoldsCombined_numeric.fa | tail -n 1 > tmp1" %(chromosome, position, a[1]))
                
                f = open("tmp1","r")
                partb = (f.read(2))
                            
                                
                log = parta+"\t"+partb+"\t"+partb[0]
                partc = "\t".join(a[5:])
                fi.write(parta+"\t"+partb+"\t"+partb[0]+"\t"+partc+"\n")
                
                print log
            
            if a[3] == "-":              
                                
                parta = a[0]+"\t"+str(int(a[1])-2)+"\t"+a[2]
                                                            
                position = int(a[1])-2
                positionb = position -1
                os.system("extract_fasta_2.pl -c%s -b %d -e %s /home/DB/M.esculenta/V6_assembly/cassavaV6_chrAndScaffoldsCombined_numeric.fa | tail -n 1 > tmp1" %(chromosome, position, positionb))
                
                f = open("tmp1","r")
                partb = (f.read(2))
                            
                                
                log = parta+"\t"+partb+"\t"+partb+a[4]
                partc = "\t".join(a[5:])
                fi.write(parta+"\t"+partb+"\t"+partb+a[4]+"\t"+partc+"\n")
                
                print log
             
            else:
                fi.write(line)
                
    print "Done with chromosome %d " %chromosome
    fi.close()
   
    chromosome += 1

  
