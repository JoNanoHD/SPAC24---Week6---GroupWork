class User:
    def __init__(self, userId, name, address, borrowedBooks = [], reservations = [], log = [], inbox = []):
        self.userId = userId
        self.name = name
        self.address = address
        self.borrowedBooks = borrowedBooks
        self.reservations = reservations
        self.log = log
        self.inbox = inbox
        

    #Adds the given log to the books logs
    def LogEvent(self, log):
        self.log.append(log)

    #Adds mail to the user
    def RecieveMail(self, mail):
        self.inbox.append(mail)

    #Check whether the user has any mail
    def HasMail(self):
        return not (not self.inbox)

    #Remove all mails from user
    def RemoveAllMail(self):
        self.inbox = []


    #Borrow book by bookId
    def BorrowBook(self, bookId):
        self.borrowedBooks.append(bookId)

    #Return book by bookId
    def ReturnBook(self, bookId):
        self.borrowedBooks.remove(bookId)

    #Reserve book by bookId
    def ReserveBook(self, bookId):
        self.reservations.append(bookId)

    #Unreserve book by bookId
    def UnreserveBook(self, bookId):
        self.reservations.remove(bookId)


    #Check wether the user has the given book
    def HasBook(self, bookId):
        return bookId in self.borrowedBooks
    
    #Checks if the user has no reservations
    def NoReservation(self):
        return not self.reservations
    
    #Check if the user has no borrowed book
    def NoBorrowedBooks(self):
        return not self.borrowedBooks

    