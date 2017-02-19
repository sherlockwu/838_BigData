import subprocess

for i in range(1, 201, 1):
	cmd1 = 'cp /u/k/a/kanwu/private/anhai/stage1/text_xin/Text_Data/file_' + str(i) + '_* ./text_200/'
	cmd2 = 'cp /u/k/a/kanwu/private/anhai/stage2/kan_marks/nlp_output/file_' + str(i) + '_* ./text_200/'

	print(cmd1)
	print(cmd2)
	subprocess.run(cmd1, shell=True)
	subprocess.run(cmd2, shell=True)
