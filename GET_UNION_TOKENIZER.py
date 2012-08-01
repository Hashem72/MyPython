#!/software/bin/python2.7

#note: try using /software/bin/python2.7  for running your python code!

import sys
import os
import commands

memory   = 22000
memory   = str(memory)
chrs = ['chr1', 'chr2']
#chrs = ['chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']
RGLAB_MAPPABLE_FILE = "/nfs/th_group/hk3/MAPPABLE_DATA_HG19/MAPPABLE_COMPARISIONS/RGLAB_hg18.K27.mappable_only.bed"
WU_MAPPABLE_FILE = "/nfs/th_group/hk3/MAPPABLE_DATA_HG19/MAPPABLE_COMPARISIONS/UW_hg18.K27.mappable_only.bed"



path =  os.path.dirname(RGLAB_MAPPABLE_FILE)
for chr in chrs:
    print "chromosome " + chr + " is under action!"
    Output_file = path+"/"+chr+".results"
    print "when job is done, you can see the result here: "+ Output_file
    RG_chr_specific_file = path+"/RG_"+chr+".bed"
    UW_chr_specific_file = path+"/UW_"+chr+".bed"
    cmd1 = 'grep -e "^'+chr+'\t" '+  RGLAB_MAPPABLE_FILE+' > '+RG_chr_specific_file
    cmd2 = 'grep -e "^'+chr+'\t" '+  WU_MAPPABLE_FILE+' > '+UW_chr_specific_file
    commands.getstatusoutput(cmd1) #run first command
    commands.getstatusoutput(cmd2) #run second command
    cmd3 = 'bsub -o '+chr+'_%J.output -e '+chr+'_%J.err -M'+memory+'000 -R"select[mem>'+memory+'] rusage[mem='+memory+']" /software/bin/python2.7 /nfs/users/nfs_h/hk3/My_Python/GET_UNION_OF_FEATURES_MAIN.py '+ UW_chr_specific_file+' '+RG_chr_specific_file +' '+ Output_file
    commands.getstatusoutput(cmd3) #send jobs 
    #print cmd3

