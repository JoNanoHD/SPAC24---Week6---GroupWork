
import pandas as pd

class ReadFile: 
    #################    
    ### SINGLETON ###
    #################
    # initialisation checks for instance and only initialises the actual object if there are no other instances
    __instance  = None
    def  __init__(self):
        if ReadFile.__instance is None:
            ReadFile.__instance = ReadFile.__impl()  
        #self.__dict__['_DataFrame_instance'] = DataFrame.__instance
        
    #redirects any function calls to the inner class __impl
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
    
    #Actual code goes in this inner class
    class __impl:
        def __init__(self):
            pass
        data = pd.read_excel('Modern_Library_Top_100_Best_Novels.xlsx')
        data = data[['TITLE','AUTH','YEAR']]
        data['AVAILABLE'] = True
        data['RESERVATIONS'] = [[] for _ in range(len(data))]
        data['LOG'] = [[] for _ in range(len(data))]
        
        data.to_excel('libraryBooks.xlsx',index=False)
            
        # Test function to check ID
        def spam(self):
            return id(self)
        
        
df = ReadFile().data