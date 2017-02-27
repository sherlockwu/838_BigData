import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn import tree

from ExtractorAndFeatureGenerator import getFeatureSet, contains


def readFilesAndTrain(input_dir,test_dir,output_file_name,stats_file):

    txtfiles = []
    testfiles = []
    output_file = open(output_file_name,'w')

    # looping extract all files
    for fname in os.listdir(input_dir):
        txtfiles.append(fname)

    for f_name in os.listdir(test_dir):
        testfiles.append(f_name)

    feature_set = []
    category = []
    train_set = []
    test_set = []

    for fname in txtfiles:
        input_file = input_dir + fname
        training_dataset = getFeatureSet(input_file, output_file)
        #train_set.append(getFeatureSet(input_file, output_file))
        for data in training_dataset:
            feature_set.append(data.feature)
            category.append(data.category)
            train_set.append(data)

    for fname in testfiles:
        input_file = test_dir + fname
        training_dataset = getFeatureSet(input_file, output_file)
        #train_set.append(getFeatureSet(input_file, output_file))
        for data in training_dataset:
            test_set.append(data)

    output_file.close()

def train_with_classifier(classifier,name,train_set,test_set,stats_file):
    category = []
    train_feature_set = []
    for data in train_set:
        train_feature_set.append(data.feature)
        category.append(data.category)
    classifier = classifier.fit(train_feature_set, category)
    result = print_result(classifier, test_set, name, stats_file,False)
    return result


def trainingAndTest(train_set,test_set,stats_file):
    decision_tree_classifier = tree.DecisionTreeClassifier()
    best_classifer = decision_tree_classifier
    stats_file = open(stats_file,'w')

    bestpnr = train_with_classifier(decision_tree_classifier, 'DECISION_TREE', train_set, test_set, stats_file)
    name = 'DECISION_TREE'

    random_forest_classifier = RandomForestClassifier()
    pnr = train_with_classifier(random_forest_classifier, 'RANDOM_FOREST', train_set, test_set, stats_file)

    if(pnr[0] > bestpnr[0]):
        best_classifer = random_forest_classifier
        name = 'RANDOM_FOREST'
        bestpnr = pnr

    svc = SVC()
    pnr = train_with_classifier(svc, 'SUPPORT_VECTOR_MACHINE', train_set, test_set, stats_file)

    if(pnr[0] > bestpnr[0]):
        best_classifer = svc
        name = 'SUPPORT_VECTOR_MACHINE'
        bestpnr = pnr

    linear_regression = LinearRegression()
    pnr = train_with_classifier(linear_regression,'LINEAR_REGRESSION',train_set,test_set,stats_file)

    if(pnr[0] > bestpnr[0]):
        best_classifer = linear_regression
        name = 'LINEAR_REGRESSION'
        bestpnr = pnr

    logistic_regression = LogisticRegression()
    pnr = train_with_classifier(logistic_regression,'LOGISTIC_REGRESSION',train_set,train_set,stats_file)

    if(pnr[0] > bestpnr[0]):
        best_classifer = logistic_regression
        name = 'LOGISTIC_REGRESSION'
        bestpnr = pnr

    stats_file.close()
    return best_classifer,name

def postProcess(predict, param):
    predict[0] = 0 if contains(param.value, ['Japan','Tokyo','America','Country','Wikipedia','City','Town','Academy','Island']) == True else predict[0]
    return predict

def print_result(classifier, test_set,name,stats_file,openStatsFile):
    if(openStatsFile):
        stats_file = open(stats_file,'w')
    ppEp = 0
    ppEn = 0
    pnEp = 0
    pnEn = 0
    postive = 0
    for i in range(0,len(test_set)):
        predict = classifier.predict(test_set[i].feature)
        predict = postProcess(predict, test_set[i])
        #print train_set[i].value,train_set[i].feature, name + ' - Predicted Value - ' + str(predict) + ' Expected Value - ' + str(train_set[i].category)
        string = test_set[i].value, test_set[i].feature, name + ' - Predicted Value - ' + str(
            predict) + ' Expected Value - ' + str(test_set[i].category)
        if test_set[i].category == 1:
            postive += 1
        if predict[0] == 1 and test_set[i].category == 1:
            ppEp += 1
        elif predict[0] == 1 and test_set[i] .category== 0:
            ppEn += 1
            stats_file.write(str(string) + "\n")
        elif predict[0] == 0 and test_set[i].category == 1:
            pnEp += 1
        elif predict[0] == 0 and test_set[i].category == 0:
            pnEn += 1
    #print name , len(test_set)
    try:
        precision = (ppEp) * 100 / (ppEp + ppEn)
    except Exception:
        precision = 0
    recall = ppEp * 100 / postive
    print name , ':Precision - ' , str(precision)
    print name , ':Recal - ' , str(recall)
    stats_file.write(name + ' - ppEp -'+ str(ppEp) + "\n")
    stats_file.write(name + ' - ppEn -'+ str(ppEn) + "\n")
    stats_file.write(name + ' - pnEp -'+ str(pnEp) + "\n")
    stats_file.write(name + ' - pnEn -'+ str(pnEn) + "\n")
    stats_file.write(name + ':Precision - '+ str(precision) + "\n")
    stats_file.write(name + ':Recal - '+ str(recall) + "\n")
    if openStatsFile:
        stats_file.close()

    return precision,recall

#readFilesAndTrain('/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage2/textFile/','/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage2/trainset2.txt')
#readFilesAndTrain('/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/inputFiles/',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/testset/',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/output2.txt',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/stats_file.txt')