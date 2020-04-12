from datetime import datetime

class SteamScraper:
    _baseUrl = 'https://steamcommunity.com/market/search/render/?query=&norender=1&start={}&count={}&search_descriptions=0&sort_column=price&sort_dir=asc&appid={}'
    _totalCount = 15027
    _maxItemsPerRequest = 100
    _gameID = 0
    _startPointer = 1;
    _dir = None
    
    def __init__(self, gameID):
        self._gameID = gameID
        
    def setTotalCount(totalCount):
        self.totalCount = totalCount
        
    def getStartPointer(self):
        return self._startPointer
    
    def createNewDir(self):
        self._dir = datetime.now().strftime(str(self._gameID) + "_%Y-%m-%d_%H:%M:%S")
    
    def getDir(self):
        return self._dir
    
    def nextPointer(self):        
            self._startPointer += 100
            
    def getUrl(self):
        finalUrl = ""
        if(self._startPointer < self._totalCount):
            finalUrl = self._baseUrl.format(self._startPointer, self._maxItemsPerRequest, self._gameID)
            
        return finalUrl