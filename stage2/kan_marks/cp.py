
import subprocess

for i in range(1, 201, 1):
	cmd = 'cp /u/k/a/kanwu/private/anhai/stage1/text_xin/Text_Data/file_' + str(i) + '_* ./texts/'
	print(cmd)
	subprocess.run(cmd, shell=True)
