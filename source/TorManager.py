import time
import logging

from RequestManager import RequestManager
from stem.control import Controller
from stem import Signal
from stem import SocketError
from stem.connection import PasswordAuthFailed
#from stem import CircStatus

class TorManager(RequestManager):
        
    _proxies = proxies = {'http': 'socks5://127.0.0.1:9050',
                          'https': 'socks5://127.0.0.1:9050'}
    
    _wait = 0
        
    def __init__(self):
        super().__init__(self._proxies)
           
    def newOnionPath(self):
        with Controller.from_port(port = 9051) as controller:
            try:
                controller.authenticate(password = "2020")
                logging.info("Successfully connected to TOR")
            except (SocketError, PasswordAuthFailed) as x:
                logging.error("Unable to connect to TOR SOCKS proxy on port 9051: {}. Is Service running correctly and on port 9050?".format(x))
                
            if self._wait > 0:
                logging.info("TOR allows a new identity in {} Seconds...".format(self._wait))
                time.sleep(self._wait)
            controller.signal(Signal.NEWNYM)
            self._wait = int(controller.get_newnym_wait())+1
        logging.info("New TOR route establised. ")
        
        self.newSession(self._proxies)