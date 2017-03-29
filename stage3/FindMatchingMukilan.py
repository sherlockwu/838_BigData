import pandas as pd

table1 = pd.read_csv('anime_1.csv').values.tolist()
table2 = pd.read_csv('animePlayer.csv').values.tolist()
set = set()

for row in table1:
    #print row
    #print str(row[1])
    set.add(str(row[1]))

output = open('animePlayerFilter.csv','w')
header = 'ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating'
output.write(header + "\n")
for row in table2:
    titletoFind = str(row[1])
    for title in set:
        if titletoFind in title:
            output.write(str(row)[1:-1] + "\n")
            break
output.close()
