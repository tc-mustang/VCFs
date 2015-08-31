#!/usr/bin/env/python -w

import sys
import re
import os
from itertools import islice


lista = list()

chromosome = 1


while chromosome <19:

    print "solving problems on chromosome %d" %(chromosome)
        
    VCFs = "/home/DB/M.esculenta/VCF_V6/correct_VCF/indel/chr%s_indel.vcf" %(chromosome)
        
    with open(VCFs) as f:
            head = list(islice(f, 11))
            
            fi = open("chr%s_correct.vcf"%(chromosome), 'w')
            
            for elements in head:
                fi.write(elements)
            
            for line in f:
                a = line.split()
                
                if a[2] not in lista:
                    fi.write(line) 
                
                lista.append(a[2])
    print " done with chromosome %d" %chromosome        
    fi.close()
    chromosome += 1                                                                                                                               
