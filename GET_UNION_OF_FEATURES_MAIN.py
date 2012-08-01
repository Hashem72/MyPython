#!/software/bin/python2.7

#note: try using /software/bin/python2.7  for running your python code!

import sys
import os
import commands
import numpy
import time

print numpy.version.version



import GET_UNION_OF_FEATURES

arg = sys.argv
    
UW_mappable_file = arg[1]
RGLAB_mappable_file = arg[2]
result_file         = arg[3]
res_file = open(result_file,'w')

print result_file

UW_coverage    = GET_UNION_OF_FEATURES.get_coverage(UW_mappable_file)
RGLAB_coverage = GET_UNION_OF_FEATURES.get_coverage(RGLAB_mappable_file)
intersect      = UW_coverage.intersection(RGLAB_coverage)
UW_not_RG      = UW_coverage.difference(RGLAB_coverage)
RG_not_UW      = RGLAB_coverage.difference(UW_coverage)
union          = UW_coverage.union(RGLAB_coverage)
inter_len      = len(intersect)
U_not_R_len    = len(UW_not_RG)
R_not_U_len    = len(RG_not_UW)
union_len      = len(union)
del UW_coverage
del RGLAB_coverage
del intersect 
del UW_not_RG
del RG_not_UW
res_file.write("intersection\t UW_but_not_RG\t RG_but_not_UW\t union\n ")
one_line =GET_UNION_OF_FEATURES.get_percentage(inter_len, U_not_R_len, R_not_U_len, union_len) 
#str(inter_len)+"\t"+str(U_not_R_len)+"\t"+str(R_not_U_len)+"\t"+str(union_len)+ "\n"
res_file.write(one_line)
res_file.close()
#print "intersection: ", inter_len, " UW and not RG: ", U_not_R_len, " RG and not UW: ", R_not_U_len, "union: ",  union_len 
sys.exit()





