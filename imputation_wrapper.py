#!/usr/bin/env python

#The correct procedure involves candles, the sacrifice of rum, tobacco and a living chicken, then invoking the following ritual chant 
#
#FILTER AND PHASE VCF files
#
# run as super user and set "ulimit -n 100000
#
#Roberto Lozano : rjl278@cornell.edu


import sys
import os

num = 1


while num <2:
    print "Proccesing chromosome %d "%num
    
    #os.system("mkdir chr%d" %num)
    os.system("ln -s ../igdBuildWithV6_hapmap_20150404_withRef_filter_chr%d.vcf chr%d/chr%d.vcf" %(num,num,num))
    
    ####### Keep only Lukas individuals:
    
    os.system("head -n 1 /home/DB/M.esculenta/Lucas_Dosage/cassava2_chr%d.snps.txt\ .imputed.txt > chr%d/markers_nonordered.txt" %(num,num))
    
    os.system("magic.py chr%d/markers_nonordered.txt > chr%d/markers" %(num,num))
    
    os.system("awk -F\"\t\" '{print $1}' /home/DB/M.esculenta/Lucas_Dosage/cassava2_chr%d.snps.txt\ .imputed.txt | tail -n +2  > chr%d/IDs" %(num,num))
    
    os.system("sed -i 's/\./:/' chr%d/IDs" %num)
    
    ####### filter by LUKAS and min read depth:
    
    os.system("vcftools --vcf chr%d/chr%d.vcf --snps chr%d/markers --keep chr%d/IDs --minDP 5 --max-alleles 2 --min-alleles 2 --recode --out chr%d/chr%d_filt.vcf" %(num,num,num,num,num,num))
    
    os.system("grep -vP \"\t-\t\" chr%d/chr%d_filt.vcf.recode.vcf > chr%d/chr%d_toimpute.vcf" %(num,num,num,num))
    
    ####### Phase/Impute
    
    #os.system("cp /home/DB/M.esculenta/VCF_V6/chr2/beagle.r1396.jar chr%d/" %(num))
    
    #os.system("java -Xmx16000m -jar beagle.r1396.jar gt=/home/DB/M.esculenta/VCF_V6/chr%d/chr%d_toimpute.vcf phase-its=5 nthreads=3 out=/home/DB/M.esculenta/VCF_V6/chr%d/imputed" %(num,num,num))
    
    #os.system("vcftools --gzvcf chr%d/imputed.vcf.gz --plink --out chr%d/plink" %(num,num))
    
    #os.system("awk '{print NR \"\t\" $0}' chr%d/plink.ped | awk '{$2=\"\";gsub(FS \"+\",FS)}1' | awk '$5=1' | awk '$6=1' > chr%d/modified.ped" %(num,num))
    
    #os.system("plink1.9 --map chr%d/plink.map --ped chr%d/modified.ped --blocks --out chr%d/" %(num,num,num))
    
    
    print "Done with chromosome %d " %num
    num += 1
