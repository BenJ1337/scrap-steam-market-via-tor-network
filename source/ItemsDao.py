import logging
import os
import sqlite3
from ProgrammStateVars import ProgrammStateVars
from os import path
from ItemsLoader import ItemsLoader

class ItemsDao():
    
    _sqliteDBName = "steamItems.db"
    _pathToDB = path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, _sqliteDBName)
    _connection = None
    _itemTable = "item"
    _priceTable = "price"
    _gameTable = "game"
    
    def __init__(self):
        self._connection = sqlite3.connect(self._pathToDB)
        logging.info("Successful connected")
        
    def closeConnection(self):        
        self._connection.close()
        
    def createItemTable(self):
        tableItems = ("CREATE TABLE IF NOT EXISTS {} ("
                       " id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
                       " type TEXT, icon_url TEXT, "
                       " icon_url_large TEXT, "
                       "  timestamp TEXT"
                       ");").format(self._itemTable)
        self._connection.execute(tableItems)
        self._connection.commit()
        
    def createPriceTable(self):
        tableItems = ("CREATE TABLE IF NOT EXISTS {} ("
                       " id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       " sell_listings INTEGER, "
                       " sell_price_text TEXT, "
                       " sale_price_text TEXT, "
                       " instance_id TEXT, "
                       " tadable_after TEXT, "
                       " tradable TEXT, "
                       " currency TEXT, "
                       " class_id INTEGER, "
                       " commodity TEXT, "
                       " market_tradable_restrictions TEXT, "
                       " timestamp TEXT"
                       ");").format(self._priceTable)
        self._connection.execute(tableItems)
        self._connection.commit()
        
    def createGameTable(self):
        tableItems = ("CREATE TABLE IF NOT EXISTS {} ("
                       " id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "app_name TEXT, "
                      " app_id INTEGER, "
                      " app_icon TEXT, "
                      " timestamp TEXT"
                       ");").format(self._gameTable)
        self._connection.execute(tableItems)
        self._connection.commit()
        
        
    def insertItem(self, item, timestamp):        
        insertItem = ("INSERT INTO {} ("
                      "name, sell_listings, sell_price_text, sale_price_text, app_name, timestamp"
                      ") VALUES ("
                      "'{}', {}, '{}', '{}', '{}', '{}'"
                      ")").format(self._itemsTable, item['name'].replace('\'', '"'), item['sell_listings'], item['sell_price_text'].replace('\'', '"'), item['sale_price_text'].replace('\'', '"'), item['app_name'].replace('\'', '"'), timestamp)
        self._connection.execute(insertItem)
        self._connection.commit()
        
    def findItemWithTimestamp(self, item, timestamp):
        selectItem = ("SELECT "
                      "name, sell_listings, sell_price_text, sale_price_text, app_name, timestamp"
                      "FROM {}"
                      "WHERE name={] "
                      "AND sell_listings={} "
                      "AND sell_price_text={} "
                      "AND sale_price_text={} "
                      "AND app_name={} "
                      "AND timestamp={} "
                      ).format(self._itemsTable, item['name'].replace('\'', '"'), item['sell_listings'], item['sell_price_text'].replace('\'', '"'), item['sale_price_text'].replace('\'', '"'), item['app_name'].replace('\'', '"'), timestamp)
        return self._connection.execute(selectItems)
        
    def getAllItems(self):        
        selectItems = ("SELECT "
                       "id, name, sell_listings, sell_price_text, sale_price_text, app_name, timestamp"
                       " FROM {}").format(self._itemTable)
        return self._connection.execute(selectItems)
    
    def getItemsByName(self, name):
        selectItems = ("SELECT "
                       "id, name, sell_listings, sell_price_text, sale_price_text, app_name, timestamp"
                       " FROM {} WHERE "
                       "name LIKE '%{}%'").format(self._itemTable, name)
        itemsCursor = self._connection.execute(selectItems)
    
        itemsDict = {}
        for item in itemsCursor:
            nameKey = item[1].replace(' ' , '')
            if (nameKey not in itemsDict):
                itemsDict[nameKey] = {}
                itemsDict[nameKey]['sell_listings'] = [item[2]]
                itemsDict[nameKey]['sell_price_text'] = [item[3]]
                itemsDict[nameKey]['sale_price_text'] = [item[4]]
                itemsDict[nameKey]['app_name'] = item[4]
                itemsDict[nameKey]['name'] = item[1]
            else:
                itemsDict[nameKey]['sell_listings'].append(item[2])
                itemsDict[nameKey]['sell_price_text'].append(item[3])
                itemsDict[nameKey]['sale_price_text'].append(item[4])
                
        return itemsDict
                
            
        
               
        


if "__main__" == __name__:
    print("Setup Logging...")
    FORMAT = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        
    print("Start Programm...")
    itemsLoader = ItemsLoader()
    itemsDao = ItemsDao()
        
    itemsDao.createItemTable()
        
    """
    itemsLoader.buildFileList()
    for datenpunktPointer in range(0, itemsLoader.getAnzahlDatenpunkte()):
        anzahlDateienDesDatenpunktes = itemsLoader.getAnzahlDateienDesDatenpunktes(datenpunktPointer)
        timestamp = itemsLoader.getTimestampVonDatenpunkt(datenpunktPointer)
        for dateiInDatenpunkt in range(0, anzahlDateienDesDatenpunktes):
            items = itemsLoader.get100ItemsVonDatenpunkt(datenpunktPointer, dateiInDatenpunkt)
            print("Datenpunkt: {}, Datei: {}".format(datenpunktPointer, dateiInDatenpunkt))
            for item in items:
                itemsDao.insertItem(item, timestamp)
    """
    items = itemsDao.getItemsByName("Special Agent Ava")
    for key in items.keys():
        print(items[key]['name'])
        print(items[key]['sell_listings'])
        print(items[key]['sell_price_text'])
        print(items[key]['sale_price_text'])
        break
    
    itemsDao.closeConnection()
    
    print("Programm finished successfully.")