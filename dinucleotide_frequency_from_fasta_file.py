import sys
from Bio import SeqIO


fasta_file_name = ''
if len(sys.argv) == 1: 
    print "expects a fasta file as argument!"
    exit
else:
    fasta_file_name = sys.argv[1]

handle = open(fasta_file_name, "rU")
nucleotides = {"A":0, "C":0, "G":0, "T":0} 
dinucleotides  = {"AA":0, "AC":0, "AG":0, "AT":0,
                  "CA":0, "CC":0, "CG":0, "CT":0,
                  "GA":0, "GC":0, "GG":0, "GT":0,
                  "TA":0, "TC":0, "TG":0, "TT":0}
for record in SeqIO.parse(handle,"fasta"):
    sequence = record.seq
    l = len(sequence)
    for i in range(0,l):
        one_nt = sequence[i]
        nucleotides[one_nt] = nucleotides[one_nt] + 1
        if  i < l-2 :
            one_dint = sequence[i:i+2]
            one_dint = str(one_dint)
            dinucleotides[one_dint] += 1
            
handle.close()

for x in nucleotides:
    print x , nucleotides[x]
    
for y in dinucleotides:
    print y, dinucleotides[y]
