import re, sys, os

def extract_file(file_name, output_file):
	#file_name = sys.argv[1]
	print('Extracting: ' + file_name)
	f = open(file_name)
	text = str(f.read())
	
	# ID (Rank)
		# <span class="dark_text">Ranked:</span>  #2852<sup>2</sup>
	m_extract = re.search(r'#(.*)\<sup\>',text)
	m_filter = re.sub(r'#', '', m_extract.group(0))
	m_filter = re.sub(r'\<sup\>', '', m_filter)
	RANK = m_filter
	#print('Ranked:' + m_filter)
	
	# Title
		# <title> </title>
	
	m_extract = re.search(r'\<title\>\n(.*)net', text)
	m_filter = re.sub(r' \-(.*)net', '', m_extract.group(0))
	m_filter = re.sub(r'\<title\>\n', '', m_filter)
	TITLE = m_filter
	#print('Title:' + m_filter)
	
	# Episodes
		#<span class="dark_text">Episodes:</span> 26
	
	m_extract = re.search(r'\>Episodes:(.*)\n(.*)', text)
	m_filter = re.sub(r'\>Episodes(.*)\n', '', m_extract.group(0))
	m_filter = re.sub(r'  ', '', m_filter)
	EPISODES = m_filter
	#print('Episodes:' + m_filter)
	
	# Producers 
		#<span class="dark_text">Producers:</span>
      		#<a href="http://myanimelist.net/anime.php?p=31">Geneon Universal Entertainment</a><sup>L</sup>,     <a href="http://myanimelist.net/anime.php?p=37">Studio Deen</a>,     <a href="http://myanimelist.net/anime.php?p=82">Marvelous Entertainment</a>,     <a href="http://myanimelist.net/anime.php?p=145">TBS</a></div>
	m_extract = re.search(r'\>Producers:(.*)\n(.*)div\>', text)
	m_filter = re.sub(r'\>Pro(.*)\n', '', m_extract.group(0))
	m_filter = re.sub(r'\<a href(.*?)\>', '', m_filter)
	m_filter = re.sub(r'\<\/a\>(.*?),', ',', m_filter)
	m_filter = re.sub(r'\<\/a\>(.*?)\<\/div\>', '', m_filter)
	m_filter = re.sub(r'     ', ' ', m_filter)
	m_filter = re.sub(r'  ', '', m_filter)
	m_filter = re.sub(r', ', '\', \'', m_filter)
	m_filter = '[\'' + m_filter + '\']'
	PRODUCERS = m_filter
	#print('Producers:' + m_filter)
	
	# Genres
		# same with producers
	m_extract = re.search(r'\>Genres:(.*)\n(.*)div\>', text)
	m_filter = re.sub(r'\>Gen(.*)\n', '', m_extract.group(0))
	m_filter = re.sub(r'\<a href(.*?)\>', '', m_filter)
	m_filter = re.sub(r'\<\/a\>(.*?),', ',', m_filter)
	m_filter = re.sub(r'\<\/a\>(.*?)\<\/div\>', '', m_filter)
	m_filter = re.sub(r'  ', '', m_filter)
	m_filter = re.sub(r', ', '\', \'', m_filter)
	m_filter = '[\'' + m_filter + '\']'
	GENRES = m_filter
	#print('Genres:' + m_filter)
	
	
	# Type
		# Type:</span> TV
	m_extract = re.search(r'Type:(.*)', text)
	m_filter = re.sub(r'Type(.*) ', '', m_extract.group(0))
	TYPE = m_filter
	#print('Type:' + m_filter)
	
	# Year
		# Aired:</span>
  		# Oct 7, 2004 to Mar 31, 2005
	m_extract = re.search(r'Aired:\<\/span\>\n(.*)\n', text)
	m_filter = re.sub(r'Aired(.*?)\n', '', m_extract.group(0))
	m_filter = re.sub(r'\n', '', m_filter)
	m_filter = re.sub(r' to(.*?), ', ',', m_filter)
	m_filter = re.sub(r' (.*?), ', '', m_filter)
	year_begin = re.sub(r',(.*)', '', m_filter)
	year_end = re.sub(r'(.*),', '', m_filter)
	PREMIERED = year_begin
	END = year_end
	#print('Premiered:' + year_begin)
	#print('END:' + year_end)
	
	# Rating
		# Rating:</span>
		# PG-13 - Teens 13 or older
	m_extract = re.search(r'Rating:\<\/span\>\n(.*)\n', text)
	m_filter = re.sub(r'Rating(.*?)\n', '', m_extract.group(0))
	m_filter = re.sub(r'\n', '', m_filter)
	m_filter = re.sub(r' \-(.*)', '', m_filter)
	m_filter = re.sub(r'  ', '', m_filter)
	RATING = m_filter
	#print('Rating:' + m_filter)
	
	# Score
		# Score:</span>
  		# <span itemprop="ratingValue">7.56</span>
	m_extract = re.search(r'Score:\<\/span\>\n(.*)\n', text)
	m_filter = re.sub(r'Score(.*?)\n', '', m_extract.group(0))
	m_filter = re.sub(r'\n', '', m_filter)
	m_filter = re.sub(r'\<span(.*?)\>', '', m_filter)
	m_filter = re.sub(r'\<\/span(.*)', '', m_filter)
	m_filter = re.sub(r'  ', '', m_filter)
	SCORE = m_filter
	#print('Score:' + m_filter)
	
	
	# voice actors
		# voice actors to table staff
	m_extract = re.search(r'Voice Actors([\s\S]*)\<a name=\"staff\"\>', text)
	# delete character tr
	#m_filter = re.searc(r'\<td valign="top" width="27"([\s\S]*?) \<tr\>align=\"right\"', '', m_extract.group(0))
	pattern = re.compile(r'\<a(.*)\<\/a\>\<br \/\>')
	m_filter = str(pattern.findall(m_extract.group(0)))
	m_filter = re.sub(r' href(.*?)\>', '', m_filter)
	m_filter = re.sub(r',', '', m_filter)
	m_filter = re.sub(r'\' \'', '\', \'', m_filter)
	VOICEACTORS = m_filter
	#print('Voice Actors:' + m_filter) 
	
	This_entry = RANK +',' + TITLE + ',' + EPISODES + ',\"' + PRODUCERS + '\",\"' + GENRES + '\",' + TYPE + ',' + PREMIERED + ',' + END + ',' + RATING + ',' + SCORE + ',\"' + VOICEACTORS + '\"\n' 

	output_file.write(This_entry)



if __name__=='__main__':
	# print help
	if len(sys.argv)!=3:
		print('Usage: python extract.py [input_dir] [output_name]')
		exit(-1)
	
	# get the input_dir
	input_dir = sys.argv[1]
	output_file = open(sys.argv[2],'w')
	
	# print out the header
	header = 'Rank,Title,Episodes,Producers,Genres,Type,PremieredYear,ENDYear,Rating,Score,VoiceActors\n'
	output_file.write(header)
	
	htmlfiles = []
	
	# looping extract all files
	for fname in os.listdir(input_dir):
		htmlfiles.append(fname)
	
	for fname in htmlfiles:
		input_file = input_dir + fname
		extract_file(input_file, output_file)
