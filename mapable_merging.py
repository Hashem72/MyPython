#!/software/bin/python2.7

#note: try using /software/bin/python2.7  for running your python code!

import sys
import os
import re
from time import datetime


stime = datetime.now()
mapable = open("/nfs/th_group/hk3/MAPPABLE_DATA_HG19/UCSC_MAPABLE/wgEncodeCrgMapabilityAlign36mer_chr1.wig", "r")
header_line = mapable.readline()
first_line  = mapable.readline()
firt_chro, first_start, first_end, first_score = first_line.split()
second_line  = mapable.readline()
second_chro, second_start, second_end, second_chro =second_line.split()
first_start =  int(first_end)
second_start = int(second_start)
if not first_end == second_start:
    print first_end, second_start

    counter = 0

while not first_end == second_start:
    counter = counter+1
    print counter
    first_line = second_line
    second_line = mapable.readline()
    firt_chro, first_start, first_end, first_score = first_line.split()
    f = mapable.readline()
    #ignore those lines start with #bedGraph
    while ( f.startswith("#bedGraph") ):
        f = mapable.readline()
    second_line = f
    second_chro, second_start, second_end, second_chro =second_line.split();

    first_start =  int(first_end)
    second_start = int(second_start)

print "firt_line"+first_line
print "second_line"+second_line

mapable.close()
etime = datetime.now()
dif_time = etime-stime
print "time for the function run is:"
print dif_time
sys.exit("job done") 
