import os, sys
import xml.etree.cElementTree as ET 
import re

if __name__ == '__main__':
	nlp_name = sys.argv[1]
	print("processing " + nlp_name + '\n')
	# readin
	nlp_tree = ET.ElementTree(file=nlp_name)
	nlp_set = set()
	last_NNP = False
	word_last = ''	
	for elem in nlp_tree.iter(tag='token'):
	# find all NNP in xml,
		pos = elem.find('POS').text
		#if (pos== 'NNP'):
		if (re.match(r'NN*', pos)):
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
				#print('find word:' + word_last)
				last_NNP = False
				nlp_set.add(word_last)	
				# sub all NNP to <p> </p> in real 
				#pattern = re.compile(word_last)
				#sub = '<p>' + word_last + '</p>'
				#file_in = re.sub(pattern, sub, file_in)
				word_last = ''
	os.chdir('/afs/cs.wisc.edu/u/k/a/kanwu/private/anhai_838/stage2/filter_output')
	fd = open(nlp_name, 'w')
	fd.write(str(list(nlp_set)))
	fd.close()				
	#fd = open(file_name, 'w')
	#fd.write(file_in)
