import json, os, re
from os import path
from ProgrammStateVars import ProgrammStateVars



class JsonManager:
    
    _game = 'csgo'
    _regExSortFileList = r'' + _game + '_(.*)\\.json'
    
    def __init__(self):
        pass
    
    
    def main(self):
        print("Json Manager")
        index = 0
        pointer = 1
        totalCount = 15000
        
        warehouse = []
        
        dirs = os.listdir(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir))
        for dir in dirs:
            itemsDict = {}
        
            files = os.listdir(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, dir))
            files.sort(key = lambda item : int(re.findall(self._regExSortFileList, item)[0]))
            for file in files:
                localItemsDict = self.loadJson(path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, dir, file))
                itemsList = localItemsDict['results']
                for item in itemsList:
                    itemsDict[item['name']] = item
            
            warehouse.append(itemsDict)
        
        
        itemsDictKeys = warehouse[0].keys()
        for itemkey in itemsDictKeys:
            if 'Agent' in itemkey or  'Agent' in itemkey:
                try:
                    print(warehouse[0][itemkey]['name'] + ' ' + str(warehouse[0][itemkey]['sell_listings']) + ' - ' + str(warehouse[1][itemkey]['sell_listings']))
                    print(warehouse[0][itemkey]['name'] + ' ' + str(warehouse[0][itemkey]['sell_price_text']) + ' - ' + str(warehouse[1][itemkey]['sell_price_text']))
                    print()
                except:
                    print("Key nicht enhalten: " + itemkey)
            
        
        """
        while(pointer < totalCount):
            data = self.loadJson("var/730_2020-04-04_18:25:25/csgo_"+str(pointer)+".json")
            #print(data.keys())
            print(data['success'])
            print(data['start'])
            print(data['pagesize'])
            print(data['total_count'])
            print(data['searchdata'])
            for item in data['results']:
                #print(item.keys())
                print(str(index))
                index += 1
                print("Name: " + item['name'])
                #print(item['hash_name'])
                print("Anzahl im Markt: " + str(item['sell_listings']))
                #print(item['sell_price'])
                print("Buy Price: " + item['sell_price_text'])
                #print(item['app_icon'])
                #print(item['app_name'])
                #print(item['asset_description'])
                print("Sell Price: " + item['sale_price_text'])
            totalCounter = data['total_count']
            pointer += 100
        """
    def loadJson(self, filename):
        data = None
        with open(filename) as json_file:
            data = json.load(json_file)
        
        return data
    
    
    
if "__main__" == __name__:
    print("Start Programm")
    
    jsonManager = JsonManager()
    jsonManager.main()
    
    print("Programm finished successfully")