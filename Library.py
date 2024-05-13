import pandas as pd
import ReadFile
import numpy as np
import openpyxl
import string
import ast


### Class for storage of data for Books in Library.
### contains build-in functions for searching the library as well as adding and removing reservations and logging
### events. Also has functionality to write the pandas DataFrame to an excel file.
class Library:
    #################    
    ### SINGLETON ###
    #################
    # initialisation checks for instance and only initialises the actual object if there are no other instances
    __instance  = None
    def  __init__(self):
        if Library.__instance is None:
            Library.__instance = Library.__impl()  
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
        filename = 'libraryBooks.xlsx'
        # Uses Readfile.py to load data from excel file
        #LibDF = pd.read_excel(filename)
        #for i in range(len(LibDF)):
        #    #LibDF.loc[i,'AVAILABLE'] = ast.literal_eval(LibDF.loc[i,'AVAILABLE'])
        #    print(LibDF.loc[i,'RESERVATIONS'] ,'and',  [ast.literal_eval(LibDF.loc[i,'RESERVATIONS'])])
        #    LibDF.loc[i,'RESERVATIONS'] = ast.literal_eval(LibDF.loc[i,'RESERVATIONS'])
        #    LibDF.loc[i,'LOG'] = ast.literal_eval(LibDF.loc[i,'LOG'])
        LibDF = ReadFile.ReadFile().data
        
        
        # subfunction to search by title, allows lowercase queries to still succeed.
        def searchTitle(self,_input):
            sNresults = []
            for i in range(len(self.LibDF)):
                if _input in self.LibDF.iloc[i].TITLE or  _input in self.LibDF.iloc[i].TITLE.lower(): # == _input:
                    sNresults.append(self.LibDF.iloc[i])
            return sNresults

        # subfunction to search by author, allows lowercase queries to still succeed.
        def searchAuthor(self,_input):
            sAresults = []
            for i in range(len(self.LibDF)):
                if _input in self.LibDF.iloc[i].AUTH or  _input in self.LibDF.iloc[i].AUTH.lower(): #== _input:
                    sAresults.append(self.LibDF.iloc[i])
            return sAresults 

        # subfunction to search by year.
        def searchYear(self,_input):
            sYresults = []
            for i in range(len(self.LibDF)):
                if str(_input) in str(self.LibDF.iloc[i].YEAR): # == _input:
                    sYresults.append(self.LibDF.iloc[i])
            return sYresults 

        # General search function, takes 1 of 3 search method as argument as well as the search input.
        def search(self,_input, method = 'none'):
            if method == 'Title':
                return self.searchTitle(_input)
            elif method == 'Author':
                return self.searchAuthor(_input)
            elif method == 'Year':
                return self.searchYear(_input)
            elif method == 'none': 
                output = []
                output.extend(self.searchYear(_input))
                if type(_input) ==  str:
                    output.extend(self.searchTitle(_input))
                    output.extend(self.searchAuthor(_input))
                
                return output
            else:
                print('ERROR! Unknown method passed to search function: '+str(method))  
            pass
        
        # Returns a pandas.series object by inputting the index of the book in the pandas DataFrame.
        def getBook(self, index):
            return self.LibDF.iloc[index]
        
        # Returns the index of a book using the above search function, so search either by author, title or year.
        # If search returns more than 1 book, returns ID of first match.
        def getIndex(self, _input):
            gI_search = self.search(_input)
            if len(gI_search) >= 1:
                return gI_search[0].name
            else:
                print('ERROR! No search results for ' + str(_input)+' in getIndex function of library class object.')
            pass
        
        
        # Flips the boolean associated with this book in the AVAILABLE column used to keep track of whether the book
        # has been lend out or not.
        def changeAvailability(self,index, userID):
            #print(self.LibDF['AVAILABLE'][index])
            self.LibDF.loc[index,('AVAILABLE')] = not self.LibDF.loc[index,('AVAILABLE')]
            if  self.LibDF.loc[index,('AVAILABLE')] == True:
                self.newLog(index, 'Returned by user '+str(userID)+'.')
            else: 
                self.newLog(index, 'Borrowed by user '+str(userID)+'.')
            
        # Adds list element for book in the LOG column.
        def newLog(self, index, _log):
            self.LibDF.loc[index,('LOG')].append(_log)
            
        # Adds userID to the list in the RESERVATIONS column associated with book with passed index, signifying that
        # the user has reserved the book.
        def newReserve(self, index, user):
            self.LibDF.loc[index,('RESERVATIONS')].append(user)
            self.newLog(index, 'Resereved by user '+str(user)+'.')
            
        # Remove a given user from list of reservations for given book.
        def removeReservation(self, bookID, userID):
            rR_removals = []
            for i in range(len( self.LibDF['RESERVATIONS'][bookID])):
                if self.LibDF['RESERVATIONS'][bookID][i] == userID:
                    rR_removals.append(i)
            rR_removals = np.array(rR_removals)
            for j in rR_removals:
                self.LibDF['RESERVATIONS'][bookID].pop(j)
                rR_removals -=1
            self.newLog(bookID,  'User '+str(userID)+' cancelled their reservation' )

        # Check if a given user is in the list of reservations for a given book.
        def isReservedBy(self,bookID,userID):
            if userID in self.LibDF['RESERVATIONS'][bookID]:
                return True
            else:
                return False
        
        # Writes the pandas DataFrame associated with this class object to an excel file, remember to include filetype
        # (.xlsx) in the filename passed to this function.
        def WriteToExcel(self, _filename, _index):
            alphabet = list(string.ascii_lowercase)
            workbook = openpyxl.load_workbook(_filename)
            for i in range(len(self.LibDF.iloc[_index].values)):
                WTE_string = alphabet[i].upper() + str(_index+2)
                if self.LibDF.iloc[_index].values[i] == True:
                    workbook.active[WTE_string] = True
                elif self.LibDF.iloc[_index].values[i] ==False:
                    workbook.active[WTE_string] = False
                else:
                    try:
                        workbook.active[WTE_string] = self.LibDF.iloc[_index].values[i]
                    except:
                        workbook.active[WTE_string] = str(self.LibDF.iloc[_index].values[i])
            workbook.save(_filename)



        
        # Test function to check ID
        def spam(self):
            return id(self)
    pass




######################################################################
################# TESTING ############################################
######################################################################