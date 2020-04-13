import logging
import os
import sqlite3
from ProgrammStateVars import ProgrammStateVars
from os import path
from ItemsLoader import ItemsLoader

class JsonToSQLite():
    
    _sqliteDBName = "steamItems.db"
    _pathToDB = path.join(ProgrammStateVars.programmDir, ProgrammStateVars.jsonDir, _sqliteDBName)
    _connection = None
    
    def __init__(self):
        self._connection = sqlite3.connect(self._pathToDB)
        logging.info("Successful connected")
        
    def closeConnection(self):        
        self._connection.close()
        
    def createItemsTable(self):
        tableItems = ("CREATE TABLE IF NOT EXISTS items ("
                       " id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), "
                       " sell_listings INTEGER, sell_price_text VARCHAR(255), sale_price_text VARCHAR(255), "
                       " app_name VARCHAR(255)"
                       ");")
        self._connection.execute(tableItems)
        self._connection.commit()
        
    def insertItem(self, item):        
        insertItem = ("INSERT INTO items ("
                      "name, sell_listings, sell_price_text, sale_price_text, app_name"
                      ") VALUES ("
                      "'{}', {}, '{}', '{}', '{}'"
                      ")").format(item['name'], item['sell_listings'], item['sell_price_text'], item['sale_price_text'], item['app_name'])
        self._connection.execute(insertItem)
        self._connection.commit()
        
    def getAllItems(self):        
        selectItems = ("SELECT "
                       "id, name, sell_listings, sell_price_text, sale_price_text, app_name"
                       " FROM items")
        return self._connection.execute(selectItems)
        


if "__main__" == __name__:
    print("Setup Logging...")
    FORMAT = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        
    print("Start Programm...")
    itemsLoader = ItemsLoader()
    jsonToSQLite = JsonToSQLite()
        
    itemsLoader.buildFileList()
    """
    items = itemsLoader.get100ItemsVonDatenpunkt(0, 0)
    for item in items:
        jsonToSQLite.insertItem(item)
    """    
    itemsCursor = jsonToSQLite.getAllItems()
    for item in itemsCursor:
        print(item[0])
        print(item[1])
        print(item[2])
        print(item[3])
    
    jsonToSQLite.closeConnection()
    
    print("Programm finished successfully.")