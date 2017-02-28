import os
import re
import sys
from nltk.corpus import wordnet as wn

from Extract_Neg import randExtractSingleFile

def getPostives(input_file):
    positives = []
    file = open(input_file)
    text = str(file.read())
    split = text.split("<p>")
    for i in range(1,len(split)):
        positive_value = split[i].split("</p>")[0]
        #print positive_value
        positives.append(positive_value)
    return positives

def does_all_character_start_with_captial(value):
    return value.istitle()

def number_of_words(value):
    return len(value.split(" "))

def number_of_characters(value):
    return len(value) - number_of_words(value) + 1

def contains(value,array_charaters):
    for match in array_charaters:
        if(match in value):
            return True
    return False

def start_of_string(value,text,category):
    try:
        if(category == 1):
            value = '<p>' + str(value) + '</p>'
        else:
            value = '<n>' + str(value) + '</n>'
        prefix = '((\w+ ){1})' + str(value)
        post = str(value) + '(( \w+ ){1})'
        prefix = re.findall(prefix, text)
        postFix = re.findall(post, text)
        return len(prefix) == 0 or len(postFix) == 0
    except Exception as e:
        print 'Exception in Parsing  - ' , value,text
        return False

def contains_The_Prefix(value,text,category):
    if(category == 1):
        value = '<p>' + str(value) + '</p>'
    else:
        value = '<n>' + str(value) + '</n>'
    prefix = '((\w+ ){2})' + str(value)
    prefix = re.findall(prefix,text)
    if len(prefix) == 0:
        prefix = '((\w+ ){1})' + str(value)
        prefix = re.findall(prefix,text)
    for word1, word2 in prefix:
        if word1 in ['The', 'the', 'The ','the '] or word2 in ['The', 'the', 'The ','the ']:
            return True
    return False

def getNegatives(input_file):
    negatives = []
    file = open(input_file)
    text = str(file.read())
    split = text.split("<n>")
    for i in range(1,len(split)):
        negative_values = split[i].split("</n>")[0]
        #print negative_values
        negatives.append(negative_values)
    return negatives


class Train:
    def __init__(self, value , feature , category):
        self.value = value
        self.feature = feature
        self.category = category

    def __str__(self):
        string = ''
        string += self.value + ","
        for data in self.feature:
            string += str(data) + ","
        string += str(self.category)
        return string

def extractNegatives(file_name):
    return randExtractSingleFile(file_name, 2)

def getFeatureSet(file_name, output_file, feature_set):
    #print 'FileName - ' ,file_name
    for positive  in getPostives(file_name):
        data = calculateFeatures(positive, file_name, 1)
        feature_set.append(data)
        output_file.write(data.__str__() + '\n')

    for negative in getNegatives(file_name):
        train_data = calculateFeatures(negative, file_name, 0)
        feature_set.append(train_data)
        output_file.write(train_data.__str__() + '\n')

    for extracted_negatives in extractNegatives(file_name):
        train_data = calculateFeatures(extracted_negatives, file_name, 0)
        feature_set.append(train_data)
        output_file.write(train_data.__str__() + '\n')

    return feature_set


def numberofupperwords(value):
    split = value.split()
    count = 0
    for word in split:
        if word.isupper():
            count += 1
    return count


def numberOfLowerWords(value):
    split = value.split()
    count = 0
    for word in split:
        if word.islower():
            count += 1
    return count


def calculateFeatures(value, file_name, category):
    captial = 1 if does_all_character_start_with_captial(value) == True else 0
    start = 1 if start_of_string(value, str(open(file_name).read()),category) == True else 0
    contain_value = 1 if contains(value, ['The','The ','In','In ', 'A ', 'It ','\'','After', 'He','When', 'She','To','With']) == True else 0
    designation = 1 if contains(value,['King','Great','Master','Queen']) == True else 0
    prefixed_by_the = 1 if contains_The_Prefix(value,str(open(file_name).read()),category) == True else 0
    no_words = number_of_words(value)
    #no_characters = number_of_characters(value)
    number_of_upper_words = numberofupperwords(value)
    number_of_lower_words = numberOfLowerWords(value)
    try:
        pos = wn.synsets(value)[0].pos()
    except Exception:
        pos = "y"
    return Train(value,[captial,start,contain_value,designation,prefixed_by_the,ord(pos),no_words, number_of_upper_words,number_of_lower_words],category)

def process(input_dir, output_file_location):
    txtfiles = []
    for fname in os.listdir(input_dir):
        txtfiles.append(fname)
    processFiles(input_dir,txtfiles, output_file_location)

def processFiles(input_dir, txtfiles, output_file_location):
    output_file = open(output_file_location,'w')
    feature_set = []
    for fname in txtfiles:
        input_file = input_dir + fname
        getFeatureSet(input_file, output_file, feature_set)

    output_file.close()
    return  feature_set

if __name__=='__main__':
    # print help
    if len(sys.argv)!=3:
        #python animePlayerParser.py /Users/mukilanashokvijaya/Downloads/anime_planet_html/ /Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage1/animePlayer.csv
        print('Usage: python ExtractorAndFeatureGenerator.py [input_dir] [output_name]')
        exit(-1)

    process(sys.argv[1], sys.argv[2])
