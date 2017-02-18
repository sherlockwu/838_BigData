import os

# get filenames
filenames = os.listdir(path='/u/k/a/kanwu/private/anhai/stage2/kan_marks/texts')

list_fd = open('filelist', 'w')
# get line for each file
for filename in filenames:
	string_line = '/u/k/a/kanwu/private/anhai/stage2/kan_marks/texts/' + filename + '\n'
	list_fd.write(string_line)

