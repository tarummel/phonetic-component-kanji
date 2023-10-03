#!/usr/bin/env python3 

# Author: Taylor Rummel (2023)

import csv
import json
from lxml import etree
import os
import re
import time

# Expected project structure:
# 
# Kanji component-Phonetic Sets/
# - kanjivg/[00001.svg, 00002.svg, ...]
# ...
# - kanjidic2.xml
# - kpcs.py
# - phonetic-component-kanji.json
# - phonetic-component-kanji.tsv
# - phonetic-component-kanji.xml
# - ...

KANJIVG_FOLDER_PATH = './kanjivg/'
KANJIDICT2_FILE_PATH = './kanjidic2.xml'
JSON_OUTPUT_PATH = 'phonetic-component-kanji.json'
TSV_OUTPUT_PATH = 'phonetic-component-kanji.tsv'
XML_OUTPUT_PATH = 'phonetic-component-kanji.xml'

kpcs_structs = {}

# Kanji Phonetic Component Set structs
class KPCSStruct():
    def __init__(self, literal='', components=None, onyomi=None, component_only_set=None, phono_component_sets=None, super_set=None, largest_phonetic_set_size=0, phonetic_match_rate=0):
        # the string literal kanji
        self.literal = literal
        # the components pulled from KanjiVG's svgs
        self.components = [] if components is None else components
        # the on'yomi readings as defined in the kanjidic
        self.onyomi = [] if onyomi is None else onyomi
        # kanji that only share a component
        self.component_only_set = [] if component_only_set is None else component_only_set
        # lists of lists who share a phonetic component for each onyomi reading
        self.phono_component_sets = [] if phono_component_sets is None else phono_component_sets
        # list of kanji that are a super set of this kanji
        # self.super_set = [] if super_set is None else super_set
        # size of the largest phonetic component set
        self.largest_phonetic_set_size = largest_phonetic_set_size
        # percentage of phonetic component matches versus just component matches
        self.reliability_rating = phonetic_match_rate

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
    
    def to_xml(self):
        char = etree.Element('character')
        etree.SubElement(char, 'literal').text = self.literal

        components = etree.SubElement(char, 'components')
        for component in self.components:
            etree.SubElement(components, 'component').text = component
        
        onyomi = etree.SubElement(char, 'onyomi')
        for on in self.onyomi:
            etree.SubElement(onyomi, 'onyomi').text = on
        
        component_set = etree.SubElement(char, 'componentSet')
        for match in self.component_only_set:
            etree.SubElement(component_set, 'c_match').text = match
        
        phono_component_set = etree.SubElement(char, 'phonoComponentSets')
        for i, set in enumerate(self.phono_component_sets):
            for kanji in set:
                etree.SubElement(phono_component_set, 'pc_match', g=i.__str__()).text = kanji

        etree.SubElement(char, 'largestPhoneticSetSize').text = self.largest_phonetic_set_size.__str__()
        etree.SubElement(char, 'reliabilityRating').text = self.reliability_rating.__str__()

        return char
    
    def to_tsv(self):
        return

# expecting something like <g kvg:element="K"> where we want K
element_attr_regex = re.compile(r'kvg:element=\"(.*?)\"')

# various characters that aren't applicable
ignore_filter_regex = re.compile(r'[a-zA-Z0-9!,.:;?]')

# step 1: iterate through each kanjivg svg and recording the kanji and components
def load_kanjivg():
    directory = os.fsencode(KANJIVG_FOLDER_PATH)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # only base files like 09999.svg as we don't care alternative stroke orders
        if len(filename) == 9 and filename.endswith('.svg'):
            file = open(f'{KANJIVG_FOLDER_PATH}{filename}', 'r')

            # expecting something like <g kvg:element="K">
            matches = re.findall(element_attr_regex, file.read())

            # the entry point for the svg always contains itself for easy reference
            literal = matches[0]

            # various characters we want to ignore
            if ignore_filter_regex.fullmatch(literal):
                continue

            # squash duplicates
            components = list(set(matches[1:]))
            kpcs_structs[literal] = KPCSStruct(literal=literal, components=components)

# step 2: load up kanjidic and grab the onyomi readings
def load_kanjidic():
    xmlp = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(KANJIDICT2_FILE_PATH, parser=xmlp)

    # the root of the parsed xml file
    root = tree.getroot()
    onyomi_elements = []

    # in kanjidic a <character> entry is the start of a kanji entry
    for character in root.iter('character'):
        # the <literal> is the corresponding <character>'s kanji
        kanji = character.find('literal').text
        if kanji in kpcs_structs:
            # lxml's xpath is regex-like and makes finding the nested onyomi element(s) easy
            onyomi_elements = character.xpath('./reading_meaning/rmgroup/reading[@r_type="ja_on"]')
            onyomi = [element.text for element in onyomi_elements]
            kpcs_structs[kanji].onyomi = onyomi

# a Kanji's perfect_series is a list of perfect series (lists) indexed corresponding to the onyomi in the onyomi readings
def build_sorted_perfect_series(onyomi: set, series: dict[str, list[str]]) -> ([str], [[str]]):
    sorted_onyomi = []
    perfect_series = []

    # Python 3.7 supports ordered dicts so we'll utilize that to sort the list of series by length (largest first)
    series = {kanji: v for kanji, v in sorted(series.items(), key=lambda item: len(item[1]), reverse=True)}

    # add the sorted values into new lists
    for kanji, value in series.items():
        sorted_onyomi.append(kanji)
        perfect_series.append(value)

    # find and add the remaining onyomi to the end
    difference = onyomi.difference(set(sorted_onyomi))
    sorted_onyomi.extend(difference)

    return sorted_onyomi, perfect_series

# Step 3: find compound kanji by matching a kanji to other kanji that they are a component of and then determine if 
# it is a phonetic match or if there is no match (component set)
def build_sets():
    for left_k, left_v in kpcs_structs.items():
        # intermediate set for counting the number of unique kanji across all perfect sets a kanji may have
        unique_perfect_kanji = set()
        # intermediate dict for all perfect matches: "人" -> KSCMStruct( literal: "人" )
        onyomi_kanji_list = {}

        for right_k, right_v in kpcs_structs.items():
            # skip if there isnt a component match
            if left_k not in right_v.components:
                continue

            # skip itself
            if left_k == right_k:
                continue

            # Python sets squash duplicates and enables useful set operations
            left_onyomi_set = set(left_v.onyomi)
            
            # no phonetic matches means a component only case
            intersection = left_onyomi_set.intersection(set(right_v.onyomi))
            if not intersection:
                left_v.component_only_set.append(right_k)
                continue
            
            unique_perfect_kanji.add(right_k)

            # an intersection means this kanji is in a perfect set
            for onyomi in intersection:
                if onyomi in onyomi_kanji_list:
                    onyomi_kanji_list[onyomi].append(right_k)
                else:
                    onyomi_kanji_list[onyomi] = [right_k]
                
        # update the sorted onyomi and phonetic component matches
        if len(onyomi_kanji_list) > 0:
            onyomi, phono_component_sets = build_sorted_perfect_series(left_onyomi_set, onyomi_kanji_list)
            reliability_rating = len(unique_perfect_kanji) / (len(unique_perfect_kanji) + len(left_v.component_only_set))
            left_v.onyomi = onyomi
            left_v.phono_component_sets = phono_component_sets
            left_v.largest_phonetic_set_size = len(phono_component_sets[0])
            left_v.reliability_rating = round(reliability_rating, 3)

# a sub set of a super set must be smaller in length by 1 or more and must contain all elements of the sub set
def is_sub_set(origin, target):
    if not len(target) > len(origin):
        return False

    return all(item in origin for item in target)

# Step 4: find the referencess. A reference are kanji that are super sets of this one.
def generate_references():
    for left_k, left_v in kpcs_structs.items():
        for right_k, right_v in kpcs_structs.items():
            # if not is_sub_set(left_v.onyomi, right_v.onyomi):
            #     continue

            if not is_sub_set(left_v.component_only_set, right_v.component_only_set):
                continue

            for i, set in enumerate(left_v.phono_component_set):
                # the super set must contain this kanji as well as everything else
                if not is_sub_set(set + [left_k], right_v[i].phono_component_set):
                    continue
        
            left_v.super_set.append(right_k)

# final step: write the files
def write_files():
    json_list = [kpcs_structs[struct].to_json() for struct in kpcs_structs]
    # brackets make this into a valid Json Array of KPCSStructs
    json_output = '[' + ',\n'.join(json_list) + ']'

    with open(JSON_OUTPUT_PATH, 'w') as f:
        print(JSON_OUTPUT_PATH)
        f.write(json_output)

    # build the XML element by element
    root = etree.Element('kpcs')
    for kanji in kpcs_structs:
        root.append(kpcs_structs[kanji].to_xml())
    tree = etree.ElementTree(root)

    with open(XML_OUTPUT_PATH, "wb") as f:
        print(XML_OUTPUT_PATH)
        tree.write(f, encoding="UTF-8", pretty_print=True, xml_declaration=True)

    # json trick found off the web
    json_str = json.loads(json_output)

    with open(TSV_OUTPUT_PATH, 'w') as f:
        print(TSV_OUTPUT_PATH)
        dw = csv.DictWriter(f, json_str[0].keys(), delimiter='\t')
        dw.writeheader()
        dw.writerows(json_str)

if __name__ == "__main__":
    total_time = time.time()

    print('Scanning KanjiVG for components...')
    load_kanjivg()

    print('Parsing kanjidic for onyomi...')
    load_kanjidic()

    print('Searching for component / phono-component matches...')
    build_sets()

    # print('Building super sets...')
    # generate_references()

    print('Writing contents to files...')
    write_files()
        
    print(f'Done! in {time.time() - total_time}')
