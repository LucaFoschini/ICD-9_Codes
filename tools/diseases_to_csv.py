# The MIT License (MIT)
# 
# Copyright (c) 2014 Luca Foschini
#
# (A copy of the license can be found here: http://opensource.org/licenses/MIT)
# 
# Convert a txt export of Disease Codes into CSV
# Input: stdin, Ouput: stdout
#
# Usage: python tools/diseases_to_csv.py < data/Dtab12.txt  > data/Dtab12.csv
#
# Dtab12.txt can be generated with the command:
# 
# textutil -convert txt Dtab12.rtf

import re
import sys

print '"code", "description"'
subranges = {}
reading_subrange = False

for line in sys.stdin.readlines():
    code_match = re.match(r'^([EV]*[0-9][0-9\.]+)\t(.*)', line) 
    subrange_match = re.match(r'^(\[[0-9 \-\,]+\])', line)
    subrange_def_match = re.match(r'^.*fifth[- ]digit.*', line)
    learning_subrange_match = re.match(r'^([0-9])\t(.*)', line) 
    if code_match:
        reading_subrange = False
        code =  code_match.group(1)
        description =  code_match.group(2) 
        print '"%s","%s"' % (code, description)
    elif subrange_match:
        reading_subrange = False
        subcode_list = eval(re.sub(r'[0-9]-[0-9]', lambda x: str(range(int(x.group(0).split('-')[0]), int(x.group(0).split('-')[1])+1))[1:-1], line))
        for subcode in subcode_list:
            print '"%s%d","%s, %s"' % (code, subcode, description, subranges[subcode])

    elif subrange_def_match:
        reading_subrange = True
    elif reading_subrange:
        if learning_subrange_match:
            subcode =  learning_subrange_match.group(1)
            description =  learning_subrange_match.group(2) 
            #print '"%s","%s"' % (subcode, description)
            subranges[int(subcode)] = description

