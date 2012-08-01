import subprocess as sp
from numpy import *

desc_d = {}
desc_d['names'] = ['TF_Id','ArrayType','Sequence','Signal_Mean','Background_Mean',
                   'Signal_Median','Background_Median','Signal_Std',
                   'Background_Std','Flag']
desc_d['formats'] = ['S10', 'S2', 'S60', 'float', 'float',
                     'float', 'float', 'float', 'float', 'int']
tfs = ['Foxp2', 'Cebpb', 'Foxj2', 'Foxp1', 'Tcf3', 'Esr1',
       'Egr2', 'Sp1', 'Mecp2', 'Junb', 'Sox14', 'Pou3f1',
       'Foxo3', 'Tbx3', 'Foxo1', 'Nr2c1', 'Irf2', 'Foxo4', 'Gmeb2', 'Zscan20']
def rc(nucs):
    new_nucs = ''
    for nuc in nucs:
        if nuc == 'A': new_nucs += 'T'
        elif nuc == 'T': new_nucs += 'A'
        elif nuc == 'C': new_nucs += 'G'
        elif nuc == 'G': new_nucs += 'C'
    return new_nucs[::-1]
def b4(x, nucs='ACGT'):
    return (not x and 'A' or ((b4(x//4) + nucs[x % 4]).lstrip('A')))
sorted_means_all = {}
for i in range(4):
    f = open('DREAM5_PBM_Data_TrainingSet.txt')
    tfs = ['Esr1', 'Sp1', 'Foxo3', 'Irf2']
    lines = []
    for line in f:
        if line.startswith(tfs[i]):
            toks = line.split()
            lines.append(tuple(toks))
    f.close()
    desc = dtype(desc_d)
    ra = array(lines, dtype=desc)
    ff = ra['Flag'] == 0
    ra = ra[ff]
    hktf = ra[ra['ArrayType'] == 'HK']
    metf = ra[ra['ArrayType'] == 'ME']
    sorted_means_hk = sorted(zip(hktf['Signal_Mean'],
                                 hktf['Sequence']), reverse=True)
    sorted_means_me = sorted(zip(metf['Signal_Mean'],
                                 metf['Sequence']), reverse=True)
    sorted_means_all[tfs[i]] = {}
    sorted_means_all[tfs[i]]['hk'] = sorted_means_hk
    sorted_means_all[tfs[i]]['me'] = sorted_means_me

######################################################################
# scan with nmica output matrices
######################################################################
array_types = ['hk', 'me']
tfs = ['Esr1', 'Sp1', 'Foxo3', 'Irf2']
# tf
tf = tfs[1]
# array
array_type = array_types[0]
# matrix
scan_matrix_type = array_types[0]
N = 1000
scan_data = sorted_means_all[tf][array_type]
# create input data to pipe to the c++ code.
input_data = ''
for n, (a, b) in enumerate(scan_data):
    input_data += b[:60] + ' '
    input_data += str(a) + ' '
    input_data += str(n) + ' '
matrix = 'top_seqs/'+tf+'_100_'+scan_matrix_type+'_mean_pfm.txt'
pp = sp.Popen('c++/probe_score/score_probes' + ' -m ' + matrix,
              shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
so, se = pp.communicate(input_data)
output = []
for line in so.split('\n')[:-1]:
    ls = line.split()
    probe = int(ls[0])
    score = float(ls[2])
    intensity = float(ls[3])
    output.append((score, probe, intensity))
soutput = sorted(output, reverse=True)
best = [p for (s, p, i) in soutput[:N]]
plt.clf()
plt.hist(best, bins=min(N, 200))
plt.title('intensity rank of top '+str(N)+' probes by score')
print "tf:", tf
print "scan matrix:", scan_matrix_type
print "array scanned:", array_type
print "top", N, "scan scores intersect top intensities",
print len(set(best).intersection(set(range(N))))

######################################################################
# create xms motifs with nminfer
######################################################################
tf = tfs[0]
top_n = 1000
for tf in tfs:
    fname = 'top_seqs/'+tf+'_'+str(top_n)+'_hk_mean'
    g = open(fname+'.fa', 'w')
    for n, (m, s) in enumerate(sorted_means_all[tf]['hk'][:top_n]):
        g.write('>'+str(n)+';mean='+str(m)+'\n'+s[:35]+'\n')
    g.close()
    # make a bsub call...
    jobname = tf+str(top_n)+'_hk'
    job = '~/nmica-0.8.0/bin/nminfer -seqs '+fname+'.fa -numMotifs 1 -minLength 8 -maxLength 16 -out '+fname+'.xms'
    what_the_shell_sees = 'bsub -J'+jobname+' -oo '+jobname+'_out.txt'+' -eo '+jobname+'_err.txt '+"'"+job+"'"
    p = sp.Popen(what_the_shell_sees, stdout=sp.PIPE, shell=True)
    o, e = p.communicate()
    print o
    print e
    fname = 'top_seqs/'+tf+'_'+str(top_n)+'_me_mean'
    g = open(fname+'.fa', 'w')
    for n, (m, s) in enumerate(sorted_means_all[tf]['me'][:top_n]):
        g.write('>'+str(n)+';mean='+str(m)+'\n'+s[:35]+'\n')
    g.close()
    # make a bsub call...
    jobname = tf+str(top_n)+'_me'
    job = '~/nmica-0.8.0/bin/nminfer -seqs '+fname+'.fa -numMotifs 1 -minLength 8 -maxLength 16 -out '+fname+'.xms'
    what_the_shell_sees = 'bsub -J'+jobname+' -oo '+jobname+'_out.txt'+' -eo '+jobname+'_err.txt '+"'"+job+"'"
    p = sp.Popen(what_the_shell_sees, stdout=sp.PIPE, shell=True)
    o, e = p.communicate()
    print o
    print e

# 2 motif call...
p = sp.Popen('~/nmica-0.8.0/bin/nminfer -seqs '+\
                 fname+'.fa -numMotifs 2 -minLength 8 -maxLength 16 -out '+\
                 fname+'_2motif.xms', shell=True)

######################################################################
# retrieve the matrix from xms file, write to pwm/pfm
######################################################################
import xml.etree.ElementTree as etree
import os
for line in os.listdir('top_seqs/'):
    if line.endswith('xms'):
        xms_file = line
        f = open('top_seqs/'+xms_file)
        parser = etree.parse(f)
        f.close()
        r1, r2, r3, r4 = [[] for _ in range(4)]
        for thing in parser.getiterator():
            if thing.attrib.has_key("pos"):
                print thing.attrib["pos"]
                for thingy in thing.getiterator():
                    if thingy.attrib.has_key("symbol"):
                        if thingy.attrib["symbol"] == 'adenine':
                            r1.append(float(thingy.text))
                        if thingy.attrib["symbol"] == 'cytosine':
                            r2.append(float(thingy.text))
                        if thingy.attrib["symbol"] == 'guanine':
                            r3.append(float(thingy.text))
                        if thingy.attrib["symbol"] == 'thymine':
                            r4.append(float(thingy.text))
        # write to a flat pwm file 
        pwm = vstack((r1, r2, r3, r4))
        g = open('top_seqs/'+xms_file[:-4]+'_pfm.txt', 'w')
        for line in pwm:
            g.write(' '.join([str(tok) for tok in line]))
            g.write('\n')
        g.close()
        background = repeat(0.25, 4)
        pwm = (log(pwm).T - log(background)).T 
        g = open('top_seqs/'+xms_file[:-4]+'_pwm.txt', 'w')
        for line in pwm:
            g.write(' '.join([str(tok) for tok in line]))
            g.write('\n')
        g.close()

