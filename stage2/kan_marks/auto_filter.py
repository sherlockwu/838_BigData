import subprocess
import os

os.chdir('./nlp_output')
# run the cmd
filenames = os.listdir(path='.')
for filename in filenames:
	cmd = 'python ../filter.py ' + filename
	subprocess.run(cmd ,shell=True)
