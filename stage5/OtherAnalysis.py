
def getUniqueGeners(input_file):
    geners = set()
    with open(input_file, "r") as ins:
        for line in ins:
            try:
                split = line.split("[")
                g = split[2].split("]")[0].split(",")
                for i in range(0,len(g)):
                    val = g[i].replace("'","")
                    val = val.strip()
                    geners.add(val)
            except Exception :
                print("Skipped " + line)
    output = open("geners.txt","w")
    for i in range(0,len(geners)):
        val = str(geners.pop())
        print(val)
        output.write(val + "\n")
    output.close()

def getUniqueTypes(input_file):
    types = set()
    with open(input_file, "r") as ins:
        for line in ins:
            try:
                split = line.split("[")
                g = split[2].split("]")[1].split(",")[1]
                types.add(g)
            except Exception :
                print("Skipped " + line)
    output = open("types.txt","w")
    for i in range(0,len(types)):
        val = str(types.pop())
        print(val)
        output.write(val + "\n")
    output.close()


getUniqueTypes('dataset_for_analysis.csv')
