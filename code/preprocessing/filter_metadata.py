from sys import argv
import re
import numpy as np



with open(argv[1], 'r') as f, open(argv[2], 'w') as f2:
    header = f.readline()
    f2.write('Entry'+'\t'+'Signal peptide'+'\t'+'Length'+'\t'+'Kingdom'+'\t'+'Species'+'\t'+'Sequence'+'\n')
    for line in f:
        line = line.rstrip()
        entry = line.split('\t')[0]
        pattern = r'\.\.([^;]+);'
        match = re.search(pattern, line.split('\t')[1])
        if match:
            end_SP = match.group(1)
        else:
            end_SP = ''
    #str(np.nan)
        #end_SP = line.split('\t')[1].split(';')[0][-2:]
        lenght = line.split('\t')[2]
        taxonomic_lineage = line.split('\t')[3]
        l_lineage = taxonomic_lineage.split(',')
        sequence = line.split('\t')[5]
        
        c = 0
        for el in l_lineage:
            if '(kingdom)' in el:
                kingdom = (el.split('(kingdom)')[0])
                c += 1

        species = line.split('\t')[4]
        if c == 0:
            f2.write(entry + '\t'+end_SP+'\t'+lenght+'\t'+ 'Others'+'\t'+species+'\t'+sequence+'\n')
        else:
            f2.write(entry + '\t'+end_SP+'\t'+lenght+'\t'+ kingdom+'\t'+species+'\t'+sequence+'\n')







