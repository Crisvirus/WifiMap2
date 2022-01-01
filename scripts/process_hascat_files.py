import glob
from datetime import datetime
import json

DATA_FOLDER = "/home/cristi/DiverseSSD/WifiMap2/data"

f = open(DATA_FOLDER+"/cracked/dump_cristi.json")
json_data = json.load(f)
f.close()
print(len(json_data))

files = glob.glob(DATA_FOLDER + "/cracked_raw/*.result")
for file in files:
    f = open(file,'r',encoding = "ISO-8859-1")
    line = f.readline()
    parts = line.split(':')
    f.close()
    mac_raw = parts[0]
    SSID = parts[2]
    password = parts[3]
    mac_raw = mac_raw.upper()
    mac = mac_raw[0:2]+":"+mac_raw[2:4]+":"+mac_raw[4:6]+":"+mac_raw[6:8]+":"+mac_raw[8:10]+":"+mac_raw[10:12]
    to_json = {}
    to_json["SSID"] = SSID
    to_json["MAC"] = mac
    to_json["password"] = password.strip()
    
    json_data.append(to_json)


    
f = open(DATA_FOLDER + "/cracked/dump_cristi.json", "w", encoding = "ISO-8859-1")
json.dump(json_data, f)
f.close()
           