#!/software/bin/python2.7
import sys
import numpy.numarray as na
from pylab import *

################################# functions ###########################



def get_coverage(file_name):
    """this will read a bed-like file and will return the union of start to ends
    from all features in the file. please note that it is assumed that file 
    containls features from only one chromosome
    """
    coverage = set()
    file = open(file_name, 'r')
    for line in file:
        chr, str, end = line.split()
        window = range(int(str),int(end))
        coverage.update(window)
    file.close()
    print len(coverage)
    return coverage

def get_percentage(intersect,A_not_B,B_not_A,union):
    """simply get the percentage
    """
    intersect = (float(intersect)/union)*100
    intersect = round(intersect,4)
    A_not_B   = (float(A_not_B)/union)*100
    A_not_B   = round(A_not_B,4)
    B_not_A   = (float(B_not_A)/union)*100
    B_not_A   = round(B_not_A,4)
    union     = (float(union)/union)*100
    union     = round(union,4)
    as_str    = str(intersect)+"\t"+str(A_not_B)+"\t"+str(B_not_A)+"\t"+str(union)+"\n"
    return as_str

def draw_parplots(chrName):
    """this is draw barplot for each chromosome
    """
    path = "/nfs/th_group/hk3/MAPPABLE_DATA_HG19/MAPPABLE_COMPARISIONS"
    ful_file_name = path+"/"+chrName+".results"
    
    try:
        f = open(ful_file_name,"r")
    except IOError as e:
        print "Cannot open the file. Possibly data for this chromosome not exist yet!"
    lines = f.readlines()
    f.close()
    required_line = lines[1]
    inter,UnotR, RnotU, uni = required_line.split()
    labels = ["Intersection", "UW_not_RG", "RG_not_UW", "Union"]
    colors = ["r", "g", "y", "b"]
    data   = [float(inter),float(UnotR), float(RnotU), float(uni)]
    xlocations = na.array(range(len(data)))+0.1
    width =0.5
    bar(xlocations, data,  width=width, color=colors)
    yticks(range(0, 120,10))
    xticks(xlocations+ width/2, labels)
    xlim(0, xlocations[-1]+width*2)
    Title = chrName+": intersection, differences and union of mappality data: John Stam and RG Lab"
    title(Title)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    ylabel('Percentage')

    show()


def visualize_overlaps(resutlsFile,chrName):
    """this is to visualize overlaps in terms of intesection(A,B), diff(A,B),diff(B,A), union(A,B) 
    """
    try:
        f= open(resutlsFile)
    except IOError as e:
        print "Cannot open the file."
        sys.exit()
    lines = f.readlines()
    f.close()
    required_line = lines[0]
    inter, AnotB, BnotA, uni = required_line.split()
    inter = round(float(inter)/float(uni)*100,2)
    AnotB = round(float(AnotB)/float(uni)*100,2)
    BnotA = round(float(BnotA)/float(uni)*100,2)
    uni   = round(float(uni)/float(uni)*100,2)
    labels = ["Intersection", "UW_not_RG", "RG_not_UW", "Union"]
    colors = ["r", "g", "y", "b"]
    data   = [inter,AnotB, BnotA, uni]
    xlocations = na.array(range(len(data)))+0.1
    width =0.5
    bar(xlocations, data,  width=width, color=colors)
    yticks(range(0, 120,10))
    xticks(xlocations+ width/2, labels)
    xlim(0, xlocations[-1]+width*2)
    Title = chrName+": Intersection, differences and union"
    title(Title)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    ylabel('Percentage')
    show()




  

 
