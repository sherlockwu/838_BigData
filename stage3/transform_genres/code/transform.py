import csv
import re
from collections import namedtuple

# readin csv

file_out = open('test_merged.csv', 'w')

file_out.write("ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating,ProductionHouse_Merged,Genres_Merged\n");

with open('test.csv', 'rb') as csvfile:
	readin = csv.reader(csvfile)
	headings = next(readin)
	Row = namedtuple('Row', headings)
	for row in readin:
				
		row_out = ','.join(str(x) for x in row)
		# get genres
		genres = str(row[4])
		genres = re.sub(r'\'', '', genres)
		#print(genres)
		# transform
		genres_split = genres.split(',')
		genres_after = ''
		for x in genres_split:
			x = str(x)
			x = re.sub(r']', '' , x)
			x = re.sub(r'\[', '' , x)
			x = re.sub(r' ', '', x)
			genres_after = genres_after+x
		# output
		
		# get productionhouse
		production = str(row[3])
		production = re.sub(r'\'', '', production)
		# transform
		production_split = production.split(',')
		production_after = ''
		for x in production_split:
			x = str(x)
			x = re.sub(r']', '' , x)
			x = re.sub(r'\[', '' , x)
			x = re.sub(r' ', '', x)
			production_after = production_after+x
		# output
		
		# print out
		row_out = re.sub(r' \'', '', row_out)
		row_out = re.sub(r'\'', '', row_out)
		file_out.write(row_out+','+production_after+','+genres_after+'\n')

file_out.close()
