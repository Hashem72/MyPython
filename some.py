# import collections
# chroms = collections.defaultdict(str)
# with open('CBS432-0809.fasta') as f:
#     for line in f:
#         if line.startswith('>'):
#             chrom = line.split('.')[1].strip()
#             continue
#         chroms[chrom] += line.strip()
# for k, v in chroms.iteritems():
#     print k, len(v)
import sys
arg1 = sys.argv[1]
chrom = 'chr' + arg1
infile = 'Chr' + arg1 + '.bed'
f = open(infile)
pairs = []
for line in f:
    a, b, c = line.split()
    pairs.append((int(b), int(c)))
pairs = sorted(pairs)
far_right_end_point = max(pairs)[1]
windows = range(0, far_right_end_point, 10000)
pair_iterator = iter(pairs)
pair = pair_iterator.next()
window_coverages = []
for n, lhep in enumerate(windows):
    try:
        if pair == pairs[-1]: 
            break
        coverage = 0
        if (n % 1000) == 0: 
            print n
        while pair[1] < lhep: 
            pair = pair_iterator.next()
        if pair[0] > lhep + 10000:
            continue
        while pair[1] < lhep + 10000:
            coverage += pair[1] - pair[0]
            pair = pair_iterator.next()
        window_coverages.append(coverage)
    except StopIteration:
        window_coverages.append(coverage)
        break
f.close()
out_file_name = chrom + '_coverage'
g = open(out_file_name, 'w')
for n, lhep in enumerate(windows):
    line_output = chrom
    if n >= len(window_coverages): 
        line_output += '\t' + str(lhep) + '\t' + str(0)
    else:
        line_output += '\t' + str(lhep) + '\t'+  str(window_coverages[n])
    g.write(line_output + '\n')
        
