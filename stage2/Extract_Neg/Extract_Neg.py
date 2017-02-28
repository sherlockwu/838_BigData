import random
import glob


def randExtractSingleFile(input_file)
  negArray = []
  file = open(input_file)
  text = str(file.read())
  split = text.split(" ")
  



def randExtract():
  list_of_files = glob.glob('../Marks/*.txt')
  negArray = []
  for file_name in list_of_files:
    negArray.extend(randExtractSingleFile(file_name))
  return negArray
  

    
