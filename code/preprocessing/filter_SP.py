from sys import argv
import re
with open(argv[1], 'r') as f, open(argv[2], 'w') as f2:
    f.readline()
    for line in f:
        flag = line.split('\t')[1].split(';')[0]
        # Use a regular expression to check the flag pattern
        match = re.match(r'SIGNAL <?1\.\.(\d{2,})', flag)
        if match:
            number_after_dots = int(match.group(1))
            
            # Check if the number is greater than 12
            if number_after_dots >= 13:
                f2.write(line.split('\t')[0] + '\n')
        
        
        
        
        
'''        flag = line.split('\t')[1].split(';')[0] 
        #print(flag)
        if flag != 'SIGNAL 1..?':
            f2.write(line.split('\t')[0]+'\n') '''
            




    
    





