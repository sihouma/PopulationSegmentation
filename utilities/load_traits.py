import os
import json

def load_traits(DIR):
    traits = {}
    for line in open(os.path.join(DIR, 'truth.txt')):
        bits = line.split(':::')
        traits[bits[0]] = {"gender":bits[1],
                           "age_group": bits[2],
        "extraverted" : bits[3],

        "stable" : bits[4],

        "agreeable":bits[5],

        "conscientious":bits[6],
        "open": bits[7].strip('\n')}
    return traits
