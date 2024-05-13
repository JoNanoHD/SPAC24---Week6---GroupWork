import pandas as pd
from User import User
from datetime import datetime
import ast
import openpyxl
import string

class UserManagement:
    __instance  = None
    def  __init__(self):
        if UserManagement.__instance is None:
            UserManagement.__instance = UserManagement.__impl()  
        #self.__dict__['_DataFrame_instance'] = DataFrame.__instance
        
    #redirects any function calls to the inner class __impl
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
    
    #Actual code goes in this inner class
    class __impl:
        def __init__(self):
            self.filename = 'user_data.xlsx'
            self.users = pd.read_excel(self.filename)
            self.currentUser = None

        #Adds user to the database of users
        def AddUser(self, name, address):
            self.users.loc[len(self.users)] = [name, address, [], [], []]

        #Notify user who has reservation for given book by id
        def NotifyUsers(self, book):
            #userId = 0
            #Find user id from book using bookId and notify all user (in simple loop) from list of reservations in given book.
            #mail = "mail mail"
            #self.users.iloc[userId].INBOX.append(mail)
            pass


        #Borrow book for user
        def UserBorrowBook(self, bookId):
            self.currentUser.BorrowBook(bookId)
            self.LogEvent(f"Borrowed book with id: {bookId} at {self.GetTimeStamp()}")

        #Return book for user
        def UserReturnBook(self, bookId):
            self.currentUser.ReturnBook(bookId)
            self.LogEvent(f"Returned book with id: {bookId} at {self.GetTimeStamp()}")

        #Reserves Book
        def UserReserveBook(self, bookId):
            self.currentUser.ReserveBook(bookId)
            self.LogEvent(f"Reserved book with id: {bookId} at {self.GetTimeStamp()}")

        #Unreserve Book
        def UserUnreserveBook(self, bookId):
            self.currentUser.UnreserveBook(bookId)
            self.LogEvent(f"Unreserved book with id: {bookId} at {self.GetTimeStamp()}")



        #Check if user has book
        def UserHasBook(self, bookId):
            return self.currentUser.HasBook(bookId)

        #Return list of books borrowed by the user
        def BorrowedBooksByUser(self):
            return self.currentUser.borrowedBooks
        
        #Return list of books reserved by the user
        def ReservedBooksByUser(self):
            return self.currentUser.reservations

        #Check if user has any reservations
        def NoReservationsByUser(self):
            return self.currentUser.NoReservation()
        
        #Check if user has any reservations
        def NoBorrowedByUser(self):
            return self.currentUser.NoBorrowedBooks()
        
        #Checks if book is already reserved by user
        def BookAlreadyReservedByUser(self, bookId):
            return bookId in self.currentUser.reservations



        #Get current time stamp
        def GetTimeStamp(self):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return current_time

        #Log event for user, such as borrowing or returning
        def LogEvent(self, event):
            self.currentUser.LogEvent(event)

        #Initialize user from database using userId
        def LogInUser(self, userId):
            tempUser = self.users.iloc[userId]
            self.currentUser = User(userId, tempUser.NAME, tempUser.ADDRESS, ast.literal_eval(tempUser.BORROWEDBOOKS), ast.literal_eval(tempUser.RESERVATIONS), ast.literal_eval(tempUser.LOG), ast.literal_eval(tempUser.INBOX))
            self.LogEvent("Log in at " + self.GetTimeStamp())

        #Logs the user out, saving their what they've done so far
        def LogOutUser(self):
            #Gem brugere her og skriv den til dataen.
            self.LogEvent("Log out at " + self.GetTimeStamp())
            #self.saveUser()
            self.WriteToExcel(self.filename, self.currentUser.userId)
            self.currentUser = None



        #Check if id exists return.
        def UserIdExists(self, userId):
            return userId < len(self.users)
        
        #Supposedly saves user to dataframe, but doesnt works
        def saveUser(self):
            self.users.loc[self.currentUser.userId,'BORROWEDBOOKS'] = self.currentUser.borrowedBooks
            self.users.loc[self.currentUser.userId,'RESERVATIONS'] = self.currentUser.reservations
            self.users.loc[self.currentUser.userId,'LOG'] = self.currentUser.log
            self.users.loc[self.currentUser.userId,'INBOX'] = self.currentUser.inbox
             
        #Saves to excelfile
        def WriteToExcel(self, _filename, _index):
            alphabet = list(string.ascii_lowercase)
            workbook = openpyxl.load_workbook(_filename)
            for i in range(len(self.currentUser.__dict__)-1):
                WTE_string = alphabet[i].upper() + str(_index+2)
                try:
                    workbook.active[WTE_string] = list(self.currentUser.__dict__.values())[i+1]
                except:
                    workbook.active[WTE_string] = str(list(self.currentUser.__dict__.values())[i+1])
            workbook.save(_filename)

        #Reads from the excel file and changes the list of possible users to that
        def ReadExcelFile(self):
            self.users = pd.read_excel(self.filename)
            
        