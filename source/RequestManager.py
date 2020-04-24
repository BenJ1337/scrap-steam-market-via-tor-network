import requests
import time
import logging

from datetime import datetime
from ProgrammStateVars import ProgrammStateVars
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class RequestManager:
    
    _session = None
    _httpAdapter = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
        
    _httpHeader = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
                   'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    
    _delay = 15 # Delay between requests
    
    def __init__(self, proxies):
        self._session = requests.session()
        #self._session.headers.clear()
        self._session.headers.update(self._httpHeader)
        self._session.mount('https://', self._httpAdapter)
        self._session.mount('http://', self._httpAdapter)
        if(proxies != None):
            self._session.proxies = proxies
            
    def newSession(self, proxies):
        self._session = requests.session()
        logging.info("New Session created.")
        self._session.headers.clear()
        self._session.cookies.clear()
        self._session.headers.update(self._httpHeader)
        self._session.mount('https://', self._httpAdapter)
        self._session.mount('http://', self._httpAdapter)
        if(proxies != None):
            self._session.proxies = proxies
            logging.info("Proxy in session sucessfully set")

    def getCookies(self):
        return self._session.cookies
    
    def getHeader(self):
        return self._session.headers
    
    def setCookie(self, key, value, domain):
        self._session.cookies.set(key, value, domain=domain)
    
    def doRequest(self, url):
        response = None
        try:
            while(response == None): 
                timeGone = datetime.now() - ProgrammStateVars.lastRequest
                
                if (timeGone.total_seconds() > self._delay):
                    logging.info("Send Request at {}".format(ProgrammStateVars.lastRequest.strftime("%m-%d-%Y %H:%M:%S")))
                    logging.debug(self._session.headers.items())
                    logging.debug(self._session.cookies.items())
                    response = self._session.get(url)
                    duration = datetime.now() - ProgrammStateVars.lastRequest
                    logging.info("Response recieved after {} ms.".format(duration))
                    ProgrammStateVars.lastRequest = datetime.now()
                else:
                    time.sleep(1)
            return response
        except requests.exceptions.ConnectionError as x:
            logging.error(str(x))