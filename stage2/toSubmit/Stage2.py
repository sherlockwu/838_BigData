import os
import re
import sys

from ExtractorAndFeatureGenerator import processFiles
from Learning import trainingAndTest,print_result

def process(input_dir, test_input_dir,output_dir, stats_file_dir):
    #Generate P and Q trainset
    ptxtfiles = []
    qtxtfiles = []
    testfiles = []
    count = 0
    for fname in os.listdir(input_dir):
        count += 1
        if(count < 150):
            ptxtfiles.append(fname)
        else:
            qtxtfiles.append(fname)

    for files in os.listdir(test_input_dir):
        testfiles.append(files)

    p_training_feature_set = output_dir + 'PTrainingDataFeatureSet.txt'
    q_training_feature_set = output_dir + 'QTrainingTestDataFeatureSet.txt'
    test_feature_set = output_dir + 'testDataFeatureSet.txt'
    stats_file = stats_file_dir + 'QTrainingTestDataSetResults.txt'
    stats_test_file = stats_file_dir + 'testSetResults.txt'
    p_training_Set = processFiles(input_dir, ptxtfiles, p_training_feature_set)
    q_training_Set = processFiles(input_dir, qtxtfiles, q_training_feature_set)
    test_set = processFiles(test_input_dir,testfiles,test_feature_set)

    classifierDetails = trainingAndTest(p_training_Set, q_training_Set, stats_file)
    print 'Best Classifier - ' , classifierDetails[1]
    print_result(classifierDetails[0],test_set,str(classifierDetails[1]),stats_test_file,True)
    #trainingAndTest(p_training_Set,test_set,stats_test_file)

#Best Till now - TrainingDataSet3
process('/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/trainingDataSet3/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/testDataSetNew/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/')
