import subprocess
import os

os.chdir('./text_200')
# run the cmd
filenames = os.listdir(path='.')
for filename in filenames:
	cmd = 'python ../mark.py ' + filename
	subprocess.run(cmd ,shell=True)
