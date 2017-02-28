import random
import glob
import re


def randExtractSingleFile(input_file, num):
  negArray = []
  file = open(input_file)
  text = str(file.read())
  p1 = '(<n>(.*?)</n>)'
  p2 = '(<p>(.*?)</p>)'
  text = re.sub(p1+'|'+p2, '', text)
  text = re.sub('[,.;:\[\]\n\r\t()\"]', ' ', text)
  split = text.split()
  for i in range(num * 2 / 3):
    index = random.randrange(len(split))
    negArray.append(split[index])
  for i in range(num / 6):
    index = random.randrange(len(split))
    st = split[index]
    if index > 0:
      st = split[index - 1] + ' ' + st
    negArray.append(st)
  for i in range(num / 6):
    index = random.randrange(len(split))
    st = split[index]
    if index > 0:
      st = split[index - 1] + ' ' + st
    if index > 1:
      st = split[index - 2] + ' ' + st
    negArray.append(st)
  return negArray
  

# num is the number of words that we want to extract from a file
def randExtract(num):
  list_of_files = glob.glob('../Marks/*.txt')
  negArray = []
  for file_name in list_of_files:
    negArray.extend(randExtractSingleFile(file_name, num))
  return negArray
  

array = randExtract(3)
print(array)   
