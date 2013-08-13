
### this it to read the bed file containg short read tags, find how many tags  have scores greater than a "Score" and then remove lines randomly from the bed file as many as those getting score greater than the Score. eg if there are 3000 tags with scores greater than or eqaul to 3.5, then it must remove 3000 lines randomly from the file.
import sys
import os
from random import randint
from sys import stdout



if len(sys.argv) != 3:
    sys.exit( "you should pass a file (containg short read tags with bias scores in their fifth field) and a threshold as parameters to this script")
    



fn = sys.argv[1]
threshold = float(sys.argv[2])

basename = os.path.basename(fn)
dirname  = os.path.dirname(fn)
words    = basename.split("_")

#output_file_name = dirname+"/Randomly_Removed_Tags/"+words[0]+"_chr22_with_bias_scores_"+str(threshold)+".bed"
output_file_name = dirname+"/Randomly_Removed_Tags_for_Duke_with_UW_motif/"+words[0]+"_chr22_with_bias_scores_"+str(threshold)+".bed"
print "the output is: " + output_file_name


number_of_lines = 0
number_features_to_be_removed = 0
with open(fn) as f:
    for line in f:
        number_of_lines +=1
        features = line.split()
        Number_of_features = len(features)
        one_score = features[4]
        if float(one_score) >=  threshold:
            number_features_to_be_removed +=1
        #print one_score
        #print line
print "total number of tags: ", number_of_lines
print "number tags to be removed = ",  number_features_to_be_removed

randomly_selected_numbers = set()
while len(randomly_selected_numbers) < number_features_to_be_removed:
    randomly_selected_numbers.add(randint(0,number_of_lines-1))

#opf = "/nfs/th_group/hk3/UW_DNaseI_HS/Gm12878_For_Paper_Analysis/dummy_threshold.bed"
output_file = open(output_file_name, "w")
index = 0
with open(fn) as f:
    for line in f:
        if not index in randomly_selected_numbers:
            output_file.write(line)
        index +=1

output_file.close()
