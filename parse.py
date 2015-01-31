#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv

def getNameToTypeMatching(input_file):
    content = input_file.read()
    pattern = re.compile('Attribute Information(.*?)\n\n', re.DOTALL)
    names = pattern.search(content);

    pattern = re.compile('\d+.*?(\w+(?: \w+:)?)\s+(\w+)')
    names_and_types = pattern.findall(names.group(0));

    return map((lambda pair: (re.sub(r'[\n :]', '', pair[0]), pair[1])), names_and_types)

def getData(input_file):
    content = input_file.read()
    data = map((lambda line: line.split(',')), content.splitlines());

    return data

def convertDataToBoolean(types, data):
    new_data = []

    for line in data:
        new_line = []
        for i, data_point in enumerate(line):
            if types[i][1] == 'Boolean':
                if data_point == '1':
                    new_line.append('true')
                if data_point == '0':
                    new_line.append('false')
            else:
                new_line.append(data_point)

        new_data.append(new_line)

    return new_data

def addColumnLabels(types, data):
    title_line = []
    new_data = []

    for type_info in types:
        title_line.append(type_info[0])

    new_data.append(title_line)
    for line in data:
        new_data.append(line)

    return new_data

with open('zoo.names.txt') as names_file, open('zoo.data.txt') as data_file:
    names_and_types = getNameToTypeMatching(names_file)
    data = getData(data_file)
    new_data = convertDataToBoolean(names_and_types, data)
    result = addColumnLabels(names_and_types, new_data)

    with open("output.csv", "wb") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(result)

    for match in names_and_types:
        print(match)

    # for line in data:
    #     print(line)

    # for line in new_data:
    #     print(line)

    for line in result:
        print(line)
