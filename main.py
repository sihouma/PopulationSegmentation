#!/usr/bin/python
from utilities.parser_xml import parse, json_name
from sys import argv

if len(argv) < 2:
    raise Exception("Specify the path of the dataset")

script, path = argv

parse(path)

print (json_name())