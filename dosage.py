#!/usr/bin/env python

#Dosagepy format correctly the output from --extract-FORMAT-info from vcftools

import sys

vcf = sys.argv[1]

with open(vcf) as file:
        for lines in file:
                deli = "\t"
                a = lines.split("\t")
                b = deli.join(a[2:])
                c = b.rstrip()
                print "S"+a[0]+"_"+a[1]+"\t"+c


