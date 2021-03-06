from .WifiAP import WifiAP
import glob
from datetime import datetime
import json

DATA_FOLDER = "/home/cristi/DiverseSSD/WifiMap2/data"

class WifiDB:
    def __init__(self):
        self.initialise()

    def initialise(self):
        self.ESSIDList = []
        self.BSSIDDict = {}
        self.BSSIDDictJSON = {}
        self.ESSIDDict = {}
        self.fileslist = []
        self.captured = []
        self.parseKismet()
        self.parseCaptures()
        self.parsePasswords()

    def parseKismet(self):
        files = glob.glob(DATA_FOLDER + "/kismet/*.csv")
        for file in files:
            f = open(file,'r',encoding = "ISO-8859-1")
            self.fileslist.append(file)
            lines = f.readlines()
            f.close()
            for line in lines:
                try:
                    wifiap = self.parseKismetLine(line)
                    # if wifiap.ESSID not in self.ESSIDList and wifiap.ESSID != '':
                    #     self.ESSIDList.append(wifiap.ESSID)
                    if wifiap.BSSID in self.BSSIDDict:
                        self.BSSIDDict[wifiap.BSSID].update(wifiap)
                    else:
                        self.BSSIDDict[wifiap.BSSID]=wifiap
                    # if wifiap.ESSID in self.ESSIDDict:
                    #     if wifiap.BSSID in self.ESSIDDict[wifiap.ESSID]:
                    #         pass
                    #     else:
                    #         self.ESSIDDict[wifiap.ESSID].append(wifiap.BSSID)
                    # else:
                    #     self.ESSIDDict[wifiap.ESSID] = [wifiap.BSSID]
                except Exception as e: # work on python 2.x
                    print(str(e))

    def parseKismetLine(self,line):
        fields = line.split(';')
        if len(fields) < 38:
            raise Exception("Bad format for AP")

        try:
            first_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
        except:
            first_time = datetime(1970, 1, 1)

        try:
            last_time = datetime.strptime(fields[19], '%a %b %d %H:%M:%S %Y')
        except:
            last_time = datetime(1970, 1, 1)
        
        if fields[2] == "":
            fields[2] = "Hidden ESSID"
        wifiap = WifiAP(fields[2],
                        fields[3],
                        first_time,
                        last_time,
                        float(fields[24]),
                        float(fields[25]),
                        float(fields[28]),
                        float(fields[29]),
                        float(fields[32]),
                        float(fields[33]))
        return wifiap

    def parseCaptures(self):
        files = glob.glob(DATA_FOLDER + "/captures/*")
        for file in files:
            fields = file.split('_')
            ESSID = fields[1]
            BSSID = fields[2].replace("-",":")
            self.captured.append(BSSID)
            if BSSID in self.BSSIDDict:
                self.BSSIDDict[BSSID].isCaptured()
                if self.BSSIDDict[BSSID].ESSID == "Hidden ESSID" and ESSID != "":
                    self.BSSIDDict[BSSID].ESSID = ESSID
            else:
                wifiap = WifiAP(ESSID,BSSID)
                wifiap.isCaptured()
                self.BSSIDDict[BSSID] = wifiap
                # if wifiap.ESSID not in self.ESSIDList and wifiap.ESSID != '':
                #     self.ESSIDList.append(wifiap.ESSID)
                # if ESSID in self.ESSIDDict:
                #     if wifiap.BSSID in self.ESSIDDict[wifiap.ESSID]:
                #         pass
                #     else:
                #         self.ESSIDDict[wifiap.ESSID].append(wifiap.BSSID)
                # else:
                #     self.ESSIDDict[wifiap.ESSID] = [wifiap.BSSID]

    def parsePasswords(self):
        files = glob.glob(DATA_FOLDER + "/cracked/*")
        for file in files:
            f = open(file,'r',encoding = "ISO-8859-1")
            json_data = json.load(f)
            f.close()
            for entry in json_data:
                if entry['MAC'] in self.BSSIDDict :
                    self.BSSIDDict[entry['MAC']].addPassword(entry['password'])
                    if self.BSSIDDict[entry['MAC']].ESSID == "Hidden ESSID" and entry["SSID"] != "":
                        self.BSSIDDict[entry['MAC']].ESSID = entry["SSID"]
                else:
                    wifiap = WifiAP(ESSID = entry['SSID'],BSSID=entry['MAC'])
                    wifiap.addPassword(entry['password'])
                    self.BSSIDDict[entry['MAC']] = wifiap

    def getJSONDictLocation(self):
        to_json = {}
        for key in self.BSSIDDict:
            wifiap = self.BSSIDDict[key]
            if wifiap.status & 2:
                to_json[wifiap.BSSID] = wifiap.toJson()
        return to_json

    def getJSONDictAllKnown(self):
        to_json = {}
        for key in self.BSSIDDict:
            wifiap = self.BSSIDDict[key]
            if wifiap.status == 7:
                to_json[wifiap.BSSID] = wifiap.toJson()
        return to_json

