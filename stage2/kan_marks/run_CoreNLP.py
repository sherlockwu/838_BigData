import subprocess
import os

os.chdir('./nlp_output')
# run the cmd
cmd = 'java -cp "../stanford-corenlp-full-2016-10-31/*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -filelist ../filelist'

subprocess.run(cmd ,shell=True)
