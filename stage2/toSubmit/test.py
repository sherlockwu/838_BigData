import os
import re
import sys
from nltk.corpus import wordnet as wn


def contains_The_Prefix(value,text,category):
    if(value == 'Earth'):
        print 'Test'
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
        if word1 in ['The', 'the', 'The ','the ']:
            return True
    return False

print contains_The_Prefix('Earth','the <p>Earth</p>',1)
print wn.synsets('sit')[0].pos()