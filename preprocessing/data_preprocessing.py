#!/usr/bin/env python
# -*- coding: utf-8

# Import Required Libraries
import pandas as pd



#####################
# Handeling Ordinal categorical variables (These variables can be ordered)
#####################


#####################
# Handeling Nominal categorical variables (These variables can not be ordered)
#####################


def gender_to_num(gender_data):
    gender ={'M': 1, 'F':2}
    return [gender[item] for item in gender_data]
