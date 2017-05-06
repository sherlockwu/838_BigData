# get two entities, how to merge them into the final entity in E
import sys
import csv
import re

def union(set1, set2):
	# transfer to set
		# filter []
	set1 = re.sub(r'\[', '', set1)
	set1 = re.sub(r'\]', '', set1)
	set2 = re.sub(r'\[', '', set2)
	set2 = re.sub(r'\]', '', set2)
		# transform to set
	set1 = set1.split(",")
	set2 = set2.split(",")
	# union
		# union
	set_merged = str(list(set(set1) | set(set2)))
	set_merged = re.sub(r'''"''', '', set_merged)
	return set_merged

def judge_integer(string_to_test):
	if(string_to_test.isdigit()):
		return int(string_to_test)
	if(string_to_test == '?'):
		return 2017
	return -1

def split(year):
	# find -
	year = year.split("-")
	# if no 
	if(len(year) <2):
		year.append(year[0])
	# delete ' '
	year[0]= re.sub(r' ', '', year[0])
        # do something special
	year[1]= re.sub(r' ', '', year[1])
	
	# find illegal return -1
	year[0] = judge_integer(year[0])
	year[1] = judge_integer(year[1])

	return year

def union_year(year1, year2):
	# miss or not year(not [A-B/?] or A)
	startyear1, endyear1 = split(year1)
	startyear2, endyear2 = split(year2)

	# get union, choose lareger
		# start
	if(startyear1 < startyear2):
		if (startyear1 == -1):
			startyear = startyear2
		else:
			startyear = startyear1
	else:
		if (startyear2 == -1):
			startyear = startyear1
		else:
			startyear = startyear2
	if (startyear == -1):
		startyear = 'Unknown'
		
		# end
	if (endyear1 > endyear2):
		endyear = endyear1
	else:
		endyear = endyear2
	if (endyear==2017):
		endyear = '?'

	return str(startyear) + '-' + str(endyear)

def merge(entity_1, entity_player):
	result = []
		
		# Title: longer one (no miss)
	print(entity_1['Title'])
	if (len(entity_1['Title']) > len(entity_player['Title'])):
		result.append(entity_1['Title'])
	else:
		result.append(entity_player['Title'])
		
		# Episodes: choose larger one
	tmp1 = re.sub(r'\+', '', str(entity_1['Episodes']))
	tmp2 = re.sub(r'\+', '', str(entity_player['Episodes']))
	if (tmp1.isdigit()==False):
		tmp1 = 'Unknown'
	if (tmp2.isdigit()==False):
		tmp2 = 'Unknown'
	if (tmp1 == 'Unknown'):
		if (tmp2 == 'Unknown'):
			result.append('Unknown')
		else:
			result.append(entity_player['Episodes'])
	else:
		if (tmp2 == 'Unknown'):
			result.append(entity_1['Episodes'])
		else:
			if ( int(tmp1) > int(tmp2) ):
				result.append(entity_1['Episodes'])
			else:
				result.append(entity_player['Episodes'])

		# ProductionHouse merge!
	result.append(union(entity_1['ProductionHouse'], entity_player['ProductionHouse']))

		# Genres merge!
	result.append(union(entity_1['Genres'], entity_player['Genres']))

		# Type : anime1(miss)
	if(entity_player['Type']!=''):
		result.append(entity_player['Type'])
	else:
		if (entity_1['Type']==''):
			result.append('Unknown')
		else:
			result.append(entity_1['Type'])

		# Year : and
	result.append(union_year(entity_1['Year'], entity_player['Year']))

		# Rating : ainme_1
	if(entity_1['Rating']!=''):
		result.append(entity_1['Rating'])
	else:
		#if (entity_player['Rating']==''):
		#	result.append('Unknown')
		#else:
		#	result.append(entity_1['Rating'])
		result.append('Unkown')
	return result


if __name__ == "__main__":
	# read in two entities
	
	csv_1 = open('anime_1_match_nodup.csv')
	csv_player = open('animePlayer_match_nodup.csv')
	reader_1 = csv.DictReader(csv_1)
	reader_player = csv.DictReader(csv_player)

	out = open('merged_overall_nodup.csv', 'w')
	out.write('ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating\n')
	for i in range(2497):
		entity_1 = next(reader_1)
		entity_player = next(reader_player)
		print("===== iteration " + str(i))
		print(entity_1)
		print()
		print(entity_player)
	
		print()
		# use rules to generate each field

		#after_merge = str(i+1) + ',' + str(merge(entity_1, entity_player)) + '\n'
		after_merge = str(i+1)
		merged = merge(entity_1, entity_player)
		after_merge += ''', "''' + str(merged[0]) + '''", ''' + str(merged[1]) + ''', "''' + str(merged[2]) + '''", "''' + str(merged[3]) + '''", ''' + str(merged[4]) + ', ' + str(merged[5]) + ', ' + str(merged[6]) + '\n'
		out.write(after_merge)
		print("the result we get: \n" + str(after_merge))







