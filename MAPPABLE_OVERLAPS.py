#!/software/bin/python2.7

#note: try using /software/bin/python2.7  for running your python code!

import sys
import os
import time
import commands
import GET_UNION_OF_FEATURES


memory = str(4000)
chrName = "chr1"


RGLAB_MAPPABLE_FILE = "/nfs/th_group/hk3/MAPPABLE_DATA_HG19/MAPPABLE_COMPARISIONS/RGLAB_hg18.K27.mappable_only.bed"
WU_MAPPABLE_FILE = "/nfs/th_group/hk3/MAPPABLE_DATA_HG19/MAPPABLE_COMPARISIONS/UW_hg18.K27.mappable_only.bed"
cpp_binary_file = "/nfs/users/nfs_h/hk3/My_CPlusPlus/Overlaps_in_Beds/BedOverlaps"  
path =  os.path.dirname(RGLAB_MAPPABLE_FILE)
Output_file = path+"/"+chrName+"_overalps.txt"

log_dir = path+"/log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)



#delete old file if exits
if(os.path.exists(Output_file)):
    os.remove(Output_file)
    

UW_chr_specific_file = log_dir+"/UW_"+chrName+".bed"
RG_chr_specific_file = log_dir+"/RG_"+chrName+".bed"

cmd1 = 'grep -e "^'+chrName+'\t" '+  RGLAB_MAPPABLE_FILE+' > '+RG_chr_specific_file
cmd2 = 'grep -e "^'+chrName+'\t" '+  WU_MAPPABLE_FILE+' > '+UW_chr_specific_file
commands.getstatusoutput(cmd1) #run first command
commands.getstatusoutput(cmd2) #run second command


op_file = log_dir+"/"+chrName+"_%J.output"
er_file = log_dir+"/"+chrName+"_%J.err"
cpp_cmd = 'bsub -o '+op_file+' -e '+ er_file+' -M'+memory+'000 -R"select[mem>'+memory+'] rusage[mem='+memory+']" '+ cpp_binary_file+" "+UW_chr_specific_file+" "+RG_chr_specific_file+" "+Output_file
commands.getstatusoutput(cpp_cmd)

while not os.path.exists(Output_file):
    time.sleep(1)
#print cpp_cmd
GET_UNION_OF_FEATURES.visualize_overlaps(Output_file,chrName)

#clean up the log dir
files = os.listdir(log_dir)
for f in files:
    fullpath = os.path.join(log_dir,f)
    print fullpath
    os.remove(fullpath)
#os.remove(Output_file)
