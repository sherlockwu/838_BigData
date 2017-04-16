# get two entities, how to merge them into the final entity in E
import sys
import csv
import re

#def filter_fields(entity_l, entity_r):
#	fields = [entity_l.split(","), entity_r.split(",")]
#	return fields


def operate_miss(field):
	return 0

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
	set_merged = list(set(set1) | set(set2))
		# add []
	# TODO return string?
	#print("passed in set1 " + str(set1))
	#print("passed in set2 " + str(set2))
	#print("try to print " + str(type(set_merged)) + " : " + str(set_merged))
	return set_merged

def judge_integer(string_to_test):
	if(string_to_test.isdigit()):
		return int(string_to_test)
	if(string_to_test == '?'):
		return 3000
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
	
	# find illegal return 0
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
		startyear = 'Unkown'
		
		# end
	if (endyear1 > endyear2):
		endyear = endyear1
	else:
		endyear = endyear2
	if (endyear==3000):
		endyear = '?'

	return str(startyear) + '-' + str(endyear)

def merge(entity_1, entity_player):
	result = []
		
		# Title: longer one (no miss)
	if (len(entity_1['Title']) > len(entity_player['Title'])):
		result.append(entity_1['Title'])
	else:
		result.append(entity_player['Title'])
		
		# Episodes: choose larger one
	# TODO miss?  + ???? 
	#operate_miss('Episodes') 
	if ( int(entity_1['Episodes']) > int(entity_player['Episodes']) ):
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
			result.append('Unkown')
		else:
			result.append(entity_1['Type'])

		# Year : and
	result.append(union_year(entity_1['Year'], entity_player['Year']))

		# Rating : ainme_1
	result.append(entity_1['Rating'])
	if(entity_1['Rating']!=''):
		result.append(entity_1['Rating'])
	else:
		if (entity_player['Rating']==''):
			result.append('Unkown')
		else:
			result.append(entity_player['Rating'])
	
	return result


if __name__ == "__main__":
	# read in two entities
	
	csv_1 = open('animetry_1.csv')
	csv_player = open('animetry_Player.csv')
	reader_1 = csv.DictReader(csv_1)
	reader_player = csv.DictReader(csv_player)
	entity_1 = next(reader_1)
	entity_player = next(reader_player)
	
	print("l: " + str(entity_1))
	print()
	print("r: " + str(entity_player))
	
	# get each field
	print()
	# use rules to generate each field

	after_merge = merge(entity_1, entity_player)
	

	# return the new entity
	print("the result we get: \n" + str(after_merge))
