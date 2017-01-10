""" 

Provider:
This metaclass represents a mobility service provider.
The classes implementing this interface should select and analyze data coming from a 
specific provider and having a specific format.

"""

from abc import ABCMeta

class Provider ():
    
    __metaclass__ = ABCMeta

    def __init__ ():
        pass
    
    def select_data():
        """
        Query provider's data from db with some criterion
        """
        pass
    
    def get_fields():
        """
        Figure out how provider's data are organised
        """
        pass
    