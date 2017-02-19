import os, sys
import xml.etree.cElementTree as ET 
import re

if __name__ == '__main__':
	file_name = sys.argv[1]
	nlp_name = '/u/k/a/kanwu/private/anhai/stage2/kan_marks/nlp_output/' + file_name + '.xml'
	# readin
	fd = open(file_name, 'r')
	file_in = fd.read()
	fd.close()
	nlp_tree = ET.ElementTree(file=nlp_name)
	nlp_set = set()
	last_NNP = False
	word_last = ''	
	for elem in nlp_tree.iter(tag='token'):
	# find all NNP in xml,
		pos = elem.find('POS').text
		if (pos=='NNP'):
			# judge last
			if (last_NNP==False):
				word_last += elem.find('word').text
			else:
				word_last += ' '
				word_last += elem.find('word').text
			last_NNP = True
		else:
			# judge last
			if (last_NNP == True):
				if (word_last in nlp_set): 
					last_NNP = False
					word_last = ''
					continue
				print('find word:' + word_last)
				last_NNP = False
				nlp_set.add(word_last)	
				# sub all NNP to <p> </p> in real 
				pattern = re.compile(word_last)
				sub = '<p>' + word_last + '</p>'
				file_in = re.sub(pattern, sub, file_in)
				word_last = ''
				
	fd = open(file_name, 'w')
	fd.write(file_in)
