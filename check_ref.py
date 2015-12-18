#!/usr/bin/env python

import sys
import re
import os
from itertools import islice
import gzip
import subprocess

vcf = sys.argv[1];
with gzip.open(vcf, 'rb') as f, gzip.open('file.txt.gz', 'wb') as f_out:
    #file_content = f.read()
    head = list(islice(f, 11))
    for elements in head:
            f_out.write(elements)
    for line in f:
                a = line.split()
                parta = a[0:3]
                partc = a[4:]
                ref = subprocess.check_output("samtools faidx /home/DB2/Marnin/Mesculenta_305_v6.fa \"%s:%s-%s\" | tail -n 1" %(a[0], a[1], a[1]), shell=True)
                b= ref.rstrip()
                a= "\t".join(parta)
                c= "\t".join(partc)
                lines = a,b,c,"\n"
                
                f_out.write( "\t".join(lines))
                
