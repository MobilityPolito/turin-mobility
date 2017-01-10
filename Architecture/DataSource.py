"""

Real Time Data Source (RTDS):
This interface is designed to represent a real time JSON stream coming 
from some API or web scraping. Its main functions are:
    - Initialize connections (e.g HTTP session)
    - Periodically retrieve and check data
    - Insert (possibly) consistent data in the DB

"""

from abc import ABCMeta
import threading

class RTDS(threading.Thread):
    
    __metaclass__ = ABCMeta
    
    def __init__ (self):
        pass
    
    def log_message (self):
        """
        Utility method for writing log messages
        """
        pass
    
    def start_session (self):
        """
        Start HTTP session with provider's website
        """
        pass

    def get_feed(self):
        """
        Retrieve data stream
        """
        pass
    
    def check_feed(self):
        """
        Check data stream correctness and consistency
        """
        pass

    def to_DB(self):
        """
        Insert data into DB
        """
        pass
    
    def run(self):
        """
        Run thread
        """        
        pass
