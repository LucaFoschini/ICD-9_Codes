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

third_level_desc = ''
fourth_level_desc = ''
fifth_level_desc = ''

# Jaccard between strings

from collections import Counter
def approx_similarity(a, b):
    sa = set(a.lower())
    sb = set(b.lower())
    return float(len(sa.intersection(sb))) / float(len(sa.union(sb)))
    

for line in sys.stdin.readlines():
    
    # Ex. match (every line): 
    # 001     Cholera
    # 001.0   Due to Vibrio cholerae
    # 001.1   Due to Vibrio cholerae el tor
    code_match = re.match(r'^([EV]*[0-9][0-9\.]+)\t(.*)', line) 

    # Ex. match: 
    # [0-6]
    subrange_match = re.match(r'^(\[[0-9 \-\,]+\])', line)

    # Ex. match:
    # The following fifth-digit subclassification is ...
    # or:
    # Requires fifth digit to identify stage
    subrange_def_match = re.match(r'^.*fifth[- ]digit.*', line)

    # Ex. match:
    # 0       unspecified
    # 1       incomplete
    # 2       complete
    learning_subrange_match = re.match(r'^([0-9])\t(.*)', line) 
    
    if code_match:
        # stop memorizing subranges
        reading_subrange = False
        
        code =  code_match.group(1)
        if code.find('.') == -1:
            third_level_desc = code_match.group(2) 
            print '"%s","%s"' % (code, third_level_desc)
        else:
            fourth_level_desc = code_match.group(2) 
            desc = "%s; %s" % (third_level_desc, fourth_level_desc)
            # avoid redundant descriptions
            if approx_similarity(third_level_desc, fourth_level_desc) > 0.9:
                desc = fourth_level_desc
            print '"%s","%s"' % (code, desc)
        
    elif subrange_match:
        # stop memorizing subranges
        reading_subrange = False
        
        subcode_list = eval(re.sub(r'[0-9]-[0-9]', lambda x: str(range(int(x.group(0).split('-')[0]), int(x.group(0).split('-')[1])+1))[1:-1], line))
        
        for subcode in subcode_list:
            fifth_level_desc = subranges[subcode]
            desc = "%s; %s, %s" % (third_level_desc, fourth_level_desc, fifth_level_desc)
            # avoid redundant descriptions
            if approx_similarity(third_level_desc, fourth_level_desc) > 0.9:
                desc = "%s; %s" % (fourth_level_desc, fifth_level_desc)
            if approx_similarity(fourth_level_desc, fifth_level_desc) > 0.9:
                desc = "%s; %s" % (third_level_desc, fifth_level_desc)

            print '"%s%d","%s"' % (code, subcode, desc)

    elif subrange_def_match:
        # start memorizing subranges
        reading_subrange = True
    elif reading_subrange:
        # memorize one subrange
        if learning_subrange_match:
            subcode =  learning_subrange_match.group(1)
            description =  learning_subrange_match.group(2) 
            #print '"%s","%s"' % (subcode, description)
            subranges[int(subcode)] = description

