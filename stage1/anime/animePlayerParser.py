import os
import re
import sys
count = 1

def parseAndWriteTheDetail(input_file, output_file):
    global count
    #print 'Parsing File - ' + input_file
    file = open(input_file)
    text = str(file.read())
    search = re.findall(r'tableTitle(.*)',text)
    for data in search:
        #title of the anime
        title = re.findall(r'\<h5\>(.*)\<\/h5\>', data)
        if len(title) != 0:
            # type of the anime
            typeWithEpisodes = re.findall(r'\<li class=\'type\'>(.*)',data)[0].split('<')[0]
            atype = typeWithEpisodes.split("(")[0].rstrip()

            # number of episodes in the anime
            try:
                episodes = typeWithEpisodes.split("(")[1].split(" ")[0]
            except Exception as e:
                #print 'Episodes error' , typeWithEpisodes - Done
                episodes = typeWithEpisodes

            #production house of the anime
            try:
                production_house =  re.findall(r'\<\/li\>(.*)\<\/li\>', data)[0].split("<li>")[1].split("<")[0]
            except Exception as e:
                #print 'ProductionHouse error - ' , re.findall(r'\<\/li\>(.*)\<\/li\>', data)
                if len(re.findall(r'\<\/li\>(.*)\<\/li\>', data)) == 0:
                    production_house = ''
                else:
                    production_house = re.findall(r'\<\/li\>(.*)\<\/li\>', data)[0].split('>')[1]

            #years
            try:
                iconYearList = re.findall(r'\<li class=\'iconYear\'>(.*)',data)[0].split('<')
                if len(iconYearList) != 0:
                    iconYear = iconYearList[0]
            except Exception as e:
                #print 'Year error - ' , re.findall(r'\<li class=\'iconYear\'>(.*)',data) - Done
                iconYear = ''

            #rating of the anime
            try:
                rating = re.findall(r'\<div class=\'ttRating\'>(.*)',data)[0].split('<')[0]
            except Exception as e:
                rating = ''
                #print 'Rating error - ' , re.findall(r'\<div class=\'ttRating\'>(.*)',data) -- Done

            #genres of anime
            genres = '['
            for genre in str(re.findall(r'\<ul\>(.*)\<\/ul\>', data)).split("<li>"):
                if genre != "['":
                    genres += genre.split("</li>")[0] + ","
            genres = genres[:-1] + ']'

            animeDetails = str(count) +',' + title[0] + ',' + episodes + ',' + production_house + ',' + genres + ',' + atype + ',' + iconYear + ',' + rating + '\n'
            output_file.write(animeDetails)
            #print animeDetails
            count +=1

if __name__=='__main__':
    # print help
    if len(sys.argv)!=3:
        #python animePlayerParser.py /Users/mukilanashokvijaya/Downloads/anime_planet_html/ /Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage1/animePlayer.csv
        print('Usage: python animePlayerParser.py [input_dir] [output_name]')
        exit(-1)

    # get the input_dir
    input_dir = sys.argv[1]
    output_file = open(sys.argv[2],'w')

    # print out the header
    header = 'ID,Title,Episodes,ProductionHouse,Genres,Type,Year,Rating\n'
    output_file.write(header)

    htmlfiles = []

    # looping extract all files
    for fname in os.listdir(input_dir):
        htmlfiles.append(fname)

    for fname in htmlfiles:
        input_file = input_dir + fname
        parseAndWriteTheDetail(input_file, output_file)

    output_file.close()
