import glob
from datetime import datetime

DATA_FOLDER = "/home/cristi/DiverseSSD/WifiMap2/data"

def parseKismetLine(line):
    # print(line)
    fields = line.split(';')
    if len(fields) < 38:
        return False

    try:
        first_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
    except:
        first_time = datetime(1970, 1, 1)

    try:
        last_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
    except:
        last_time = datetime(1970, 1, 1)
    
    if fields[32] == "GPSBestLat":
        return False

    # print("24 :" + str(float(fields[24])))
    # print("25 :" + str(float(fields[25])))
    # print("28 :" + str(float(fields[28])))
    # print("29 :" + str(float(fields[29])))
    # print("32 :" + str(float(fields[32])))
    # print("33 :" + str(float(fields[33])))

    try:
        if float(fields[24]) == 0 and float(fields[25]) == 0 and float(fields[28]) == 0 and float(fields[29]) == 0 and float(fields[32]) == 0 and float(fields[33]) == 0:
            return False
    except:
        print("Shitty Format")
        return False
    
    return True

files = glob.glob(DATA_FOLDER + "/kismet_raw/*.csv")
kept_lines = []
for file in files:
    f = open(file,'r',encoding = "ISO-8859-1")
    lines = f.readlines()
    f.close()
    for line in lines:
        if(parseKismetLine(line)):
            kept_lines.append(line)
    
f = open(DATA_FOLDER + "/kismet/processed.csv", "w", encoding = "ISO-8859-1")
for line in kept_lines:
    f.write(line)
f.close()
            