class WifiAP:
    def __init__(self, ESSID, BSSID,firstSeen = "Unknown", lastSeen = "Unknown", GPSMinLat = 0, GPSMinLon = 0, GPSMaxLat = 0, GPSMaxLon = 0, GPSBestLat = 0, GPSBestLon = 0):
        self.ESSID = ESSID
        self.BSSID = BSSID
        self.firstSeen = firstSeen
        self.lastSeen = lastSeen
        self.GPSMinLat = GPSMinLat
        self.GPSMinLon = GPSMinLon
        self.GPSMaxLat = GPSMinLon
        self.GPSMaxLon = GPSMaxLon
        self.GPSBestLat = GPSBestLat
        self.GPSBestLon = GPSBestLon
        self.password = "Unknown"
        self.status = 0
        if GPSBestLat != 0:
            self.status = 1

        self.status_list = ["Only Seen","Location known","Only Captured","Captured and known location", "Only Password", "Password and Location", "Password and captured","All is known"]
    
    def isCaptured(self):
        self.status = self.status | 2
    
    def addPassword(self,password):
        self.password = password
        self.status = self.status | 4

    def getStatus(self):
        return self.status_list[self.status]

    def update(self, newAP):
        if newAP.GPSMinLat != 0.0 and newAP.GPSMinLat < self.GPSMinLat:
            self.GPSMinLat = newAP.GPSMinLat
        
        if newAP.GPSMinLon != 0.0 and newAP.GPSMinLon < self.GPSMinLon:
            self.GPSMinLon = newAP.GPSMinLon

        if newAP.GPSMaxLat != 0.0 and newAP.GPSMaxLat > self.GPSMaxLat:
            self.GPSMaxLat = newAP.GPSMaxLat
        
        if newAP.GPSMaxLon != 0.0 and newAP.GPSMaxLon > self.GPSMaxLon:
            self.GPSMinLon = newAP.GPSMinLon

        if self.GPSBestLat == 0.0:
            self.GPSMaxLat = newAP.GPSMaxLat

        if self.GPSBestLon == 0.0:
            self.GPSMaxLon = newAP.GPSMaxLon

        if newAP.firstSeen < self.firstSeen:
            self.firstSeen = newAP.firstSeen

        if newAP.lastSeen > self.lastSeen:
            self.lastSeen = newAP.lastSeen

    