#!/usr/bin/env python
# -*- coding: utf-8

# Import Required Libraries
import os
import json


#######
# Load the author age, sex, and personality traits
#############


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
        "open": bits[7]}
    return traits
