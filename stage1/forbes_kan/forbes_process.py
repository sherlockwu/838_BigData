import re

# prepare for reading and outputing
f = open('./forbes_list', 'r')
f_out = open('./forbes.csv', 'w')
text = str(f.read())


# filter html tags
text_1 = re.sub(r'\\r\\n\<strong\>', "\n", text)
text_2 = re.sub(r'\<\/strong\>\\r\\nNet Worth:', "\t", text_1)
text_3 = re.sub(r'B\\r\\nSource of wealth: ', "\t", text_2)

# filter units
text_4 = re.sub(r'\$', "", text_3)
text_5 = re.sub(r'(.*)\. ', "", text_4)
f_out.write('Name\tNet Worth(Billions$)\tSource of Wealth')
f_out.write(text_5)
