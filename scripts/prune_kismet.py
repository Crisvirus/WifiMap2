import glob
from datetime import datetime

DATA_FOLDER = "/home/cristi/DiverseSSD/WifiMap2/data"

def parseKismetLine(line):
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
    if float(fields[32]) == 0 or float(fields[33]) == 0:
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
            