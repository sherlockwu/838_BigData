import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from ExtractorAndFeatureGenerator import processFiles


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

def train_with_classifier(classifier,name,train_set,test_set,stats_file, openFile=False):
    category = []
    train_feature_set = []
    for data in train_set:
        train_feature_set.append(data.feature)
        category.append(data.category)
    classifier = classifier.fit(train_feature_set, category)
    result = print_result(classifier, test_set, name, stats_file,openFile)
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

def crossValidation(train_set):
    train_feature_set = []
    category = []
    for data in train_set:
        train_feature_set.append(data.feature)
        category.append(data.category)
    classifiers = []
    classifiers.append(tree.DecisionTreeClassifier())
    classifiers.append(RandomForestClassifier())
    classifiers.append(SVC(kernel='linear', C=1))
    classifiers.append(LinearRegression())
    classifiers.append(LogisticRegression())

    names = ['DECISION_TREE','RANDOM_FOREST','SUPPORT_VECTOR_MACHINE','LINEAR_REGRESSION','LOGISTIC_REGRESSION']

    max_precision = 0.0

    for i in range(0,len(classifiers)):
        if names[i] == 'LINEAR_REGRESSION':
            precision = cross_val_score(classifiers[i], train_feature_set, category, cv=3)
            recall = cross_val_score(classifiers[i], train_feature_set, category, cv=3)
            f1 = cross_val_score(classifiers[i], train_feature_set, category, cv=3)
        else:
            precision = cross_val_score(classifiers[i], train_feature_set, category, cv=3,scoring='precision')
            recall = cross_val_score(classifiers[i], train_feature_set, category, cv=3,scoring='recall')
            f1 = cross_val_score(classifiers[i], train_feature_set, category, cv=3,scoring='f1')


            total_precision = 0.0
            total_recall = 0.0
            total_f1 = 0.0
            best_precision = 0.0
            best_recall = 0.0
            best_f1 = 0.0
            for j in range(0,3):
                total_precision = total_precision + precision[j]
                total_recall = total_recall + recall[j]
                total_f1 = total_f1 + f1[j]

                if(best_precision < precision[j]):
                    best_precision = precision[j]
                if(best_recall < recall[j]):
                    best_recall = recall[j]
                if(best_f1 < f1[j]):
                    best_f1 = f1[j]
            precision_value = total_precision / float(len(precision))
            recall_value = total_recall / float(len(recall))
            f1_value = total_f1 / float(len(f1))

            print("Precision: %0.2f " % (precision.mean()))
            print("Recall: %0.2f " % (recall.mean()))
            print("F1: %0.2f " % (f1.mean()))
            print("Best Precision: %0.2f " % (best_precision))
            print("Best Recall: %0.2f " % (best_recall))
            print("Best F1: %0.2f " % (best_f1))
            if max_precision < best_precision:
                best_classifier = classifiers[i]
                best_classifier_name = names[i]
                b_recall = best_recall
                b_f1 = best_f1
                max_precision = best_precision

    return best_classifier,best_classifier_name, max_precision, b_recall,b_f1

def postProcess(predict, param):
    predict[0] = 0 if contains(param.value, ['Japan','Tokyo','America','Country','Wikipedia','City','Town','Academy','Island','Earth']) == True else predict[0]
    return predict

def print_result(classifier, test_set,name,stats_file,openStatsFile):
    if(openStatsFile):
        stats_file = open(stats_file,'w')
    ppEp = 0.0
    ppEn = 0.0
    pnEp = 0.0
    pnEn = 0.0
    postive = 0.0
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
            #stats_file.write(str(string) + "\n")
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
    stats_file.write(name + ' - ppEp ='+ str(ppEp) + "\n")
    stats_file.write(name + ' - ppEn ='+ str(ppEn) + "\n")
    stats_file.write(name + ' - pnEp ='+ str(pnEp) + "\n")
    stats_file.write(name + ' - pnEn ='+ str(pnEn) + "\n")
    stats_file.write(name + ':Precision = '+ str(precision) + "\n")
    stats_file.write(name + ':Recal = '+ str(recall) + "\n")
    stats_file.write(name + ':F1 = ' + str(( 2 * precision * recall / ( precision + recall))) + "\n")
    if openStatsFile:
        stats_file.close()

    return precision,recall

#readFilesAndTrain('/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage2/textFile/','/Users/mukilanashokvijaya/IdeaProjects/anhai_838/stage2/trainset2.txt')
#readFilesAndTrain('/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/inputFiles/',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/testset/',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/output2.txt',
#                  '/Users/mukilanashokvijaya/IdeaProjects/anhai_838_new/stage2/extarction/stats_file.txt')

#ptxtfiles = []
#input_dir = "/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/trainingDataSet3/"
#for fname in os.listdir(input_dir):
#    ptxtfiles.append(fname)
#p_training_feature_set = "/Users/mukilanashokvijaya/IdeaProjects/anhai_838_Stage2/stage2/toSubmit/sample.txt"
#p_training_Set = processFiles(input_dir, ptxtfiles, p_training_feature_set)
#validation = crossValidation(p_training_Set)
#print validation

