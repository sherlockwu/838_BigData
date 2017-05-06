# get two entities, how to merge them into the final entity in E
import sys
import csv
import re



if __name__ == "__main__":
	# read in two entities
	#ids = open('predicted_values_ids.csv')
	ids = open('predicted_values_ids_nodup.csv')
	reader_ids = csv.DictReader(ids)
	
	file_1 = open('anime_1.csv')
	file_2 = open('animePlayer.csv')
	file_1 = file_1.readlines()
	file_2 = file_2.readlines()

	out_1 = open('anime_1_match_nodup.csv','w')
	out_2 = open('animePlayer_match_nodup.csv','w')
	out_1.write('ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating,ProductionHouse_Merged,Genres_Merged\n')
	out_2.write('ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating,ProductionHouse_Merged,Genres_Merged\n')
	# fetch two tuples
	for row in reader_ids:
		out_1.write(file_1[int(row['ltable_ID'])])
		out_2.write(file_2[int(row['rtable_ID'])])
	# write into two tables
