import json
import os
import re
import logging
from os import path
from ProgrammStateVars import ProgrammStateVars



class ItemsLoader:
    
    _game = 'csgo'
    _regExSortFileList = r'' + _game + '_(.*)\\.json'
    _fileList = []
    
    def __init__(self):
        pass
    
    
    def main(self):
        print("Create File List")
        
    def buildFileList(self):
        datenpunktIndex = 0
                
        dirs = os.listdir(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir))
        for dir in dirs:
            itemsDict = {}
            if path.isdir(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, dir)):            
                logging.info("> Lade nächsten Datenpunkt.")
                self._fileList.append([])
                
                files = os.listdir(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, dir))
                files.sort(key = lambda item : int(re.findall(self._regExSortFileList, item)[0]))
                for file in files:
                    self._fileList[datenpunktIndex].append(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, dir, file))
                                
                datenpunktIndex += 1
            else:
                logging.info("Das ist kein Datenpunk!")
        for list in self._fileList:
            print(list)
        
        for list in self._fileList:
            print("Dateien im Datenpunkt: {}".format(len(list)))
        
        
    def getDatenpunk(self, pointer):
        return self._fileList[pointer]
    
    def getAnzahlDatenpunkte(self):
        return len(self._fileList)
    
    def get100ItemsVonDatenpunkt(self, datenpunkPointer, itemsPointer):
        data = self.loadJson(self._fileList[datenpunkPointer][itemsPointer])
        return data['results']
    
    def printItems(self, items):
        for item in items:
                #print(item.keys())
                print("Name: " + item['name'])
                #print(item['hash_name'])
                print("Anzahl im Markt: " + str(item['sell_listings']))
                #print(item['sell_price'])
                print("Buy Price: " + item['sell_price_text'])
                #print(item['app_icon'])
                #print(item['app_name'])
                #print(item['asset_description'])
                print("Sell Price: " + item['sale_price_text'])
        
    def loadJson(self, filename):
        data = None
        with open(filename) as json_file:
            data = json.load(json_file)
        
        return data
    
    
    
if "__main__" == __name__:
    print("Setup Logging...")
    FORMAT = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    
    print("Start Programm")
    
    itemsLoader = ItemsLoader()
    itemsLoader.buildFileList() 
    items = itemsLoader.get100ItemsVonDatenpunkt(0, 0)
    ##jsonManager.printItems(items)
    
    print("Programm finished successfully")