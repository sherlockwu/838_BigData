import os
import re
import sys

from sklearn.tree import DecisionTreeClassifier


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
            return False
    return True

def start_of_string(value,text):
    prefix = '((\w+ ){1})' + str(value)
    post = str(value) + '(( \w+ ){1})'
    prefix = re.findall(prefix, text)
    postFix = re.findall(post, text)
    return len(prefix) == 0

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

def getFeatureSet(file_name, output_file):
    trainset = []
    for positive  in getPostives(file_name):
        data = getTrainData(positive, file_name, 1)
        trainset.append(data)
        output_file.write(data.__str__() + '\n')

    for negative in getNegatives(file_name):
        train_data = getTrainData(negative, file_name, 0)
        trainset.append(train_data)
        output_file.write(train_data.__str__() + '\n')

    return trainset

def getTrainData(value,file_name,category):
    captial = 1 if does_all_character_start_with_captial(value) == True else 0
    start = 1 if start_of_string(value, str(open(file_name).read())) == True else 0
    contain_value = 1 if contains(value, ['The ', 'A ', 'It ','\'']) == True else 0
    no_words = number_of_words(value)
    no_characters = number_of_characters(value)
    return Train(value,[captial,start,contain_value,no_words,no_characters],category)

#getPostives("/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage1/text_xin/Text Data/file_202_magi-sinbad-no-bouken.txt")
#getNegatives("/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage1/text_xin/Text Data/file_202_magi-sinbad-no-bouken.txt")
#print "Mukilan ashok".istitle()

#test = ". My name is Mukilan Ashok"
#print re.findall('((\w+ ){1})My', test)
#print re.findall('My(( \w+){1})', test)
#print start_of_string("My", test)
if __name__=='__main__':
    # print help
    if len(sys.argv)!=3:
        #python animePlayerParser.py /Users/mukilanashokvijaya/Downloads/anime_planet_html/ /Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage1/animePlayer.csv
        print('Usage: python Extractor.py [input_dir] [output_name]')
        exit(-1)

    # get the input_dir
    input_dir = sys.argv[1]
    output_file = open(sys.argv[2],'w')

    txtfiles = []

    # looping extract all files
    for fname in os.listdir(input_dir):
        txtfiles.append(fname)

    for fname in txtfiles:
        input_file = input_dir + fname
        getFeatureSet(input_file, output_file)

    output_file.close()