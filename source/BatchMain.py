import time
import logging
import json

from RequestManager import RequestManager
from TorManager import TorManager
from SteamScraper import SteamScraper
from requests import Response
from datetime import datetime
from ProgrammStateVars import ProgrammStateVars
from pathlib import Path
from os import path

class BatchMain:
    
    _torManager = None
    _steamScraper = None
    _logger = None
    _torIPRatingFilename = "tor-ip-rating.json"
    
    def __init__(self):
        self._torManager = TorManager()
        self._steamScraper = SteamScraper(730)
        self._requestManager = RequestManager(None)
        self._logger = logging.getLogger('BatchMain')
        self._logger.setLevel(logging.DEBUG)
    
    def main(self):
        ProgrammStateVars.lastRequest = datetime.now()
        
        logging.debug(ProgrammStateVars.programmDir)
        self._prepareDir()
        
        steamMarketUrl = self._steamScraper.getUrl()
        realIP = self.testRealIP()
        
        torIPDict = {}        
        if(path.isfile(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, self._torIPRatingFilename))):
            torIPDict = self.loadTorIPRatingFromFile()
            
        torIP = ""
        while (steamMarketUrl != ""):
            if(torIP != "" and realIP != torIP):
                responseNormal = self._torManager.doRequest(steamMarketUrl)
                if isinstance(responseNormal, Response):
                    if(responseNormal.status_code == 200):
                        self.writeTextToFile("csgo_"+str(self._steamScraper.getStartPointer())+".json", responseNormal.text)
                        self._steamScraper.nextPointer()
                        steamMarketUrl = self._steamScraper.getUrl()
                        torIPDict[torIP]["goodReq"] += 1
                    else: # among others HTTP Status 429
                        logging.error("Steam Rest Api Request wasn't successfull status_code != 200: ".format(responseNormal.status_code))
                        logging.error("Response Text: {}".format(responseNormal.headers))
                        torIPDict[torIP]["badReq"] += 1
                        self._torManager.newOnionPath()
                        torIP = ""
                else:
                    logging.error("Returned Object of SteamAPI Request isn't a Response")
                    break
            else:
                torIP = self.testTORIP()
                if(torIP not in torIPDict):
                    torIPDict[torIP] = {"goodReq": 0, "badReq": 0}
            logging.debug(torIPDict)
                
        self.writeTorIPRatingFromFile(torIPDict)
    
    def _prepareDir(self):
        logging.debug("Create Dir \"{}\" for Dumps if not exists."
                      .format(ProgrammStateVars.jsonDir))
        # Create Base Dir for JSONs
        Path(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir)).mkdir(parents=True, exist_ok=True)
        # Create Sub Dir for current Exec
        self._steamScraper.createNewDir()
        jsonDumpsDir = self._steamScraper.getDir()
        logging.debug(
            "Create Dir \"{}\" for current run JSON-Dumps if not exists."
            .format(jsonDumpsDir)
            )      
        Path(path.join(
            ProgrammStateVars.programmDir,
            ProgrammStateVars.jsonDir,
            jsonDumpsDir)).mkdir(parents=True, exist_ok=True)

    def testTORIP(self):     
        urlForIP = 'http://blob.bplaced.net'   
        ipResponse = self._torManager.doRequest(urlForIP)
        if isinstance(ipResponse, Response):
            if(ipResponse.status_code == 200):
                logging.info("Tor IP: " + ipResponse.text)
                return ipResponse.text
            else: 
                logging.error("Request for IP not successfull status_code != 200: {}"
                              .format(ipResponse.status_code))
                logging.error("Response Text: {}".format(ipResponse.text))
        else:
            logging.error("Returned Object of Request for IP isn't a Response: {}"
                          .format(ipResponse))  
        return ""
    
    def testRealIP(self):     
        urlForIP = 'http://blob.bplaced.net'   
        ipResponse = self._requestManager.doRequest(urlForIP)
        if isinstance(ipResponse, Response):
            if(ipResponse.status_code == 200):
                logging.info("Real IP: " + ipResponse.text)
                return ipResponse.text
            else: 
                logging.error("Request for IP not successfull status_code != 200: {}"
                              .format(ipResponse.status_code))
                logging.error("Response Text: {}".format(ipResponse.text))
        else:
            logging.error("Returned Object of Request for IP isn't a Response: {}"
                          .format(ipResponse))         
        return ""
    
    def loadTorIPRatingFromFile(self):
        data = None
        with open(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, self._torIPRatingFilename)) as file:
            data = json.load(file)
        return data
    
    def writeTextToFile(self, filename, text):
        with open(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, self._steamScraper.getDir(), filename), 'w') as file:
            file.write(text)
    
    def writeTorIPRatingFromFile(self, dictJson):
        with open(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, self._torIPRatingFilename), 'w') as file:
            json.dump(dictJson, file)
            
            
        
if "__main__" == __name__:
    print("Setup Logging...")
    FORMAT = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        
    print("Start Programm...")
    
    batchMain = BatchMain()
    batchMain.main()
    
    print("Programm finished successfully.")