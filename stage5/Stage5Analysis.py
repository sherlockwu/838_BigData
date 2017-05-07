import pandas as pd

#1,"Steins;Gate",24,"[ 'Kadokawa Pictures Japan',  'Nitroplus',  'AT-X',  'White Fox',  'Movic', 'Frontier Works',  'Media Factory',  'FUNimation Entertainment', 'WHITE FOX']","[ 'Psychological',  'Time Travel',  'LGBT Themes',  'Thriller', 'Based on a Visual Novel',  'Sci Fi', 'Sci-Fi']",TV,2011-2011,4.7
def generateFeature(input_file):
    header = ""
    geners = []
    with open("geners.txt", "r") as ins:
        for line in ins:
            line = line.replace("\n","")
            geners.append(line)
            val = "is" + str(line) + ","
            header += str(val)

    types = []
    with open("types.txt", "r") as ins:
        for line in ins:
            line = line.replace("\n","")
            types.append(line)
            val = "is" + str(line) + ","
            header += str(val)

    rest = "year,rating"
    header += rest
    print(header)

    with open(input_file, "r") as ins:
        output = open("features.txt","w")
        count = 0;
        for line in ins:
            if count == 0:
                count = count + 1
            else:
                count = count + 1
                feature = calculateFeature(geners,types,line,count)
                if feature != "":
                    output.write(feature)
                #print(feature)
    output.close()

def calculateFeature(geners, types, line,count):
    try:
        feature = str(count) + ","
        split = line.split("[")
        generString = split[2].split("]")[0]
        for i in range(0,len(geners)):
            if geners[i] in generString:
                feature = feature + "1,"
            else:
                feature = feature + "0,"

        values = split[2].split("]")[1].split(",")
        for i in range(0,len(types)):
            if types[i] in values[1]:
                feature = feature + "1,"
            else:
                feature = feature + "0,"

            year = values[2].split("-")[0]
            year = year.strip()
            feature = feature + year + "," + values[3]
            return feature
    except Exception:
        print("Skipped " + line)
    return ""


generateFeature('dataset_for_analysis.csv')