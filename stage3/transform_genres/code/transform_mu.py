import csv
import re
from collections import namedtuple

# readin csv

file_out = open('animePlayer_merged.csv', 'w')

file_out.write("ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating,Genres_Merged\n");

with open('animePlayer.csv', 'rb') as csvfile:
	readin = csvfile.readlines()
	head = 1 
	for row in readin:
		if (head>0):
			head = 0
			continue	
		# for mulikan
		#print(row)
		genres_extract = re.search(r'\[(.*)]',str(row)).group(0)
		
		genres_after = re.sub(r'\[', '', genres_extract)
		genres_after = re.sub(r']', '', genres_after)
		genres_after = re.sub(r' ', '', genres_after)
		genres_after = re.sub(r',', '', genres_after)
	
		# get genres
		
		# productionHouse
		#production_after = production = str(row[3])
		
		# print out
		row_out = re.sub(r'\n', '', row)
		file_out.write(row_out+','+genres_after+'\n')

file_out.close()
