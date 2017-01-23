""" 

Provider:
This metaclass represents a mobility service provider.
The classes implementing this interface should select and analyze data coming from a 
specific provider and having a specific format.

"""

from abc import ABCMeta

class ServiceProvider ():
    
    __metaclass__ = ABCMeta

    def __init__ ():
        pass
    
    def select_data(self):
        """
        Query provider's data from db with some criterion
        """
        pass
    
    def get_fields(self):
        """
        Figure out how provider's data are organised
        """
        pass

    def get_fleet(self):
        """
        Deduce provider's fleet from snapshots
        """
        pass
    
    def update_cars_status (self):
        """
        Deduce cars' status from snapshots
        """
        pass
    
    def get_parks_and_books (self):
        """
        Create provider's books and parks collections
        """
        pass
