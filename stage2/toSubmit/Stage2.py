import os
import re
import sys

from ExtractorAndFeatureGenerator import processFiles
from Learning import train_with_classifier,print_result, crossValidation

def process(input_dir, test_input_dir,output_dir, stats_file_dir):
    #Generate P and Q trainset
    all_train_files = []
    p_txt_files = []
    q_txt_files = []
    test_files = []
    count = 0
    for fname in os.listdir(input_dir):
        count += 1
        if(count < 150):
            p_txt_files.append(fname)
        else:
            q_txt_files.append(fname)
        all_train_files.append(fname)

    for files in os.listdir(test_input_dir):
        test_files.append(files)

    all_training_feature_set = output_dir + 'AllTrainingDataFeatureSet.txt'
    p_training_feature_set = output_dir + 'PTrainingDataFeatureSet.txt'
    q_training_feature_set = output_dir + 'QTrainingTestDataFeatureSet.txt'
    test_feature_set = output_dir + 'testDataFeatureSet.txt'
    stats_file = stats_file_dir + 'QTrainingTestDataSetResults.txt'
    stats_test_file = stats_file_dir + 'testSetResults.txt'

    #Generating feature set for all the words in all the data sets
    I_training_set = processFiles(input_dir, all_train_files, all_training_feature_set)
    p_training_Set = processFiles(input_dir, p_txt_files, p_training_feature_set)
    q_training_Set = processFiles(input_dir, q_txt_files, q_training_feature_set)
    test_set = processFiles(test_input_dir,test_files,test_feature_set)

    # perform cross validation to obtain the best classifier for this purpose.
    best_classifier = crossValidation(I_training_set)
    print 'Classifier chosen - ' , best_classifier[1]
    print 'Chosen Classifier Preicsion -', best_classifier[2]
    print 'Chosen Classifier Recall -', best_classifier[3]
    print 'Chosen Classifier F1 -', best_classifier[4]

    #classifierDetails = trainingAndTest(p_training_Set, q_training_Set, stats_file)
    #print 'Best Classifier - ' , classifierDetails[1]
    #Train the chossen classifier to train on subsets P ans test on subset Q from the super set I
    train_with_classifier(best_classifier[0],str(best_classifier[1]),p_training_Set,q_training_Set,stats_file,True)

    #Use the learnt model to classify the test dataset J and print out the Precision and Accuracy
    print_result(best_classifier[0],test_set,str(best_classifier[1]),stats_test_file,True)
    #trainingAndTest(p_training_Set,test_set,stats_test_file)

#Best Till now - TrainingDataSet3
process('/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2_new/stage2/toSubmit/trainingDataSet3/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2_new/stage2/toSubmit/testDataSetNew/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2_new/stage2/toSubmit/',
        '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2_new/stage2/toSubmit/')
