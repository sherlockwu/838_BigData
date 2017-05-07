from sklearn.linear_model import LinearRegression
import math

def train(file):
    #output = open("featuresRefined.txt","w")
    featureTrain = []
    categoryTrain = []
    featureTest = []
    categoryTest = []
    count = 0
    with open(file, "r") as ins:
        for line in ins:
            try:
                split = line.split(",")
                featureVector = split[0:len(split)-1]
                featureVector = list(map(int, featureVector))
                categoryValue = float(split[len(split) -1])
                if count < 8000:
                    featureTrain.append(featureVector)
                    categoryTrain.append(categoryValue)
                else:
                    featureTest.append(featureVector)
                    categoryTest.append(categoryValue)
                #output.write(line)
            except Exception:
                print("Skipping " + line)
            count = count + 1

    #output.close()
    linear_regression = LinearRegression()
    model = linear_regression.fit(featureTrain,categoryTrain)
    pIc = 0
    pC = 0
    underPerformed = 0
    overPerformed = 0
    for i in range(0,len(featureTest)):
        output = model.predict(featureTest[i])
        print(str(output) + " : " + str(categoryTest[i]) + " --> " + str(output - categoryTest[i]))
        if math.fabs(output - categoryTest[i]) > 0.5:
            pIc += 1
            if output - categoryTest[i] > 0:
                underPerformed += 1
            else:
                overPerformed += 1
        else:
            pC += 1

    precision = pC * 100 / ( pIc + pC )
    print("Precision = " + str(precision))
    print("Predicted Incorrect = " + str(pIc))
    print("Predicted Correct = " + str(pC))
    print("OutPerformed Animes = " + str(overPerformed))
    print("UnderPerformed Animes = " + str(underPerformed))


train("featuresRefined.txt")