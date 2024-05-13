from UserManagement import UserManagement
from Library import Library
import os

userManagement = None
library = None
superSecretPassword = "password"

#Shows main menu for users
def ShowMenu():
    while True:
        os.system('cls')
        print(f"Welcome {userManagement.currentUser.name}")
        print("\nSelect one:\n")
        print("1: Search for book")
        print("2: See reservations")
        print("3: See borrowed books")
        print("4: See log")
        print("5: See mailbox")
        print("6: Log out")
        input = NumberInput(1, 6)
        match input:
            case 1:
                ShowSearchMenu()
            case 2:
                ShowReservations()
            case 3:
                ShowBorrowedBooks()
            case 4:
                ShowLogs()
            case 5:
                ShowMailbox()
            case 6:
                LogOut()
                break

#Shows main menu for admins
def ShowMenuSystem():
    while True:
        print("Welcome admin")
        print("\nSelect one:\n")
        print("1: Log out")
        print("2: Add new book to library")
        input = NumberInput(1, 2)
        match input:
            case 1:
                break
            case 2:
                AddBookToLibrary()



#Adds new book to library (Not implemented)
def AddBookToLibrary():
    KeyToContinue()
    pass


#Show the user their borrowed books
def ShowBorrowedBooks():
    if userManagement.NoBorrowedByUser():
        print("No borrowed books...")
    else:
        print("Current borrowed books: \n")
        for book in userManagement.BorrowedBooksByUser():
            bookObject = library.getBook(book)
            print(f"{bookObject.TITLE} by {bookObject.AUTH}")
    KeyToContinue()

#Shows the user their reserve books
def ShowReservations():
    if userManagement.NoReservationsByUser():
        print("No reservations...")
    else:
        print("Current resevations: \n")
        for book in userManagement.ReservedBooksByUser():
            bookObject = library.getBook(book)
            print(f"{bookObject.TITLE} by {bookObject.AUTH}")
    KeyToContinue()

#Shows the user the search menu
def ShowSearchMenu():
    os.system('cls')
    print("How would you like to search for your book?")
    print("\n1: By author\n2: by year\n3: by title\n4: By all\n5: Return to menu")
    input = NumberInput(1, 5)
    if input < 5:
        SearchMenu(input)

#Shows the user their logs
def ShowLogs():
    print("Logs:")
    for log in userManagement.currentUser.log:
        print(f"{log}")
    KeyToContinue()

#Show the user their mailbox
def ShowMailbox():
    if not userManagement.currentUser.HasMail():
        print("No mail...")
    else:
        for mail in userManagement.currentUser.inbox:
            print(f"{mail}\n")
    KeyToContinue()


#Searchh menu where you specify how and what you want to search for
def SearchMenu(searchType):
    match searchType:
        case 1:
            method = "Author"
        case 2:
            method = "Year"
        case 3:
            method = "Title"
        case 4:
            method = ""

    difParam = False
    while True:
        os.system('cls')
        print(f"Search by {method}")
        searchTerm = input("\nPlease enter searchterm: ")
        if searchTerm == "retry0":
            difParam = True
            break
        LogEvent(f"Searched for term: '{searchTerm}'")
        
        if method == "":
            books = library.search(searchTerm)
        else:
            books = library.search(searchTerm, method)

        if len(books) >= 1:
            break
        print("\nNo matches found, try again, type retry0 if you wish to search by a different parameter")

    if difParam:
        ShowSearchMenu()
        return
    
    SelectBook(books)
    #KeyToContinue()

#Here you select the book you want to view more info on
def SelectBook(books):
    os.system('cls')
    i = 1
    for book in books:
        print(f"{i}: {book.TITLE}, {book.AUTH}, {book.YEAR}")
        i += 1
    print("\nWhat book you wish to view more info on, reserve, unreserve, book or return?\nEnter 0 to return to menu")
    input = NumberInput(0, i)-1
    if input == -1:
        return
    BookAction(books[input], books)

#Here you specify what action you want to do with said book
def BookAction(book, books):
    canReserve = not userManagement.BookAlreadyReservedByUser(book.name)
    canBorrow = CanBorrowBook(book)
    canReturn = userManagement.UserHasBook(book.name)
    funcToDo = []

    os.system('cls')
    print(f"What would you like to do with {book.TITLE}")

    if  canReserve:
        print("1: reserve book")
        funcToDo.append(ReserveBook)
    else:
        print("1: unreserve book")
        funcToDo.append(UnreserveBook)

    if canBorrow:
        print("2: borrow book")
        funcToDo.append(BorrowBook)
    elif canReturn:
        print("2: return book")
        funcToDo.append(ReturnBook)

    print("3: return to list of books")

    input = NumberInput(1, 3)-1
    if input == 2:
        SelectBook(books)
    else:
        print()
        funcToDo[input](book)
    

#Check if user can borrow given book
def CanBorrowBook(book):
    if len(book.RESERVATIONS) > 0:
        if book.RESERVATIONS[0] == userManagement.currentUser.userId:
            return book.AVAILABLE
        else:
            return False
    else:
        return book.AVAILABLE

#Borrows book for user
def BorrowBook(book):
    bookId = book.name
    userManagement.UserBorrowBook(bookId)
    library.changeAvailability(bookId, userManagement.currentUser.userId)
    SaveBookToFile(bookId)
    print(f"You have borrowed {book.TITLE}")

#Returns book for user
def ReturnBook(book):
    bookId = book.name
    userManagement.UserReturnBook(bookId)
    library.changeAvailability(bookId, userManagement.currentUser.userId)
    SaveBookToFile(bookId)
    print(f"You have returned {book.TITLE}")
    NotifyReservers()

#Reserves book for user
def ReserveBook(book):
    bookId = book.name
    userManagement.UserReserveBook(bookId)
    library.newReserve(bookId, userManagement.currentUser.userId)
    SaveBookToFile(bookId)
    print(f"You have reserved {book.TITLE}")

#Unreseve book for user
def UnreserveBook(book):
    bookId = book.name
    userManagement.UserUnreserveBook(bookId)
    library.removeReservation(bookId, userManagement.currentUser.userId)
    SaveBookToFile(bookId)
    print(f"You have unreserved {book.TITLE}")


#Saves book to library file after change
def SaveBookToFile(bookId):
    library.WriteToExcel(library.filename, bookId)

#Notfies user when book is return and it has reservations
def NotifyReservers(book):
    #userManagement.NotifyUsers(book)
    pass

#Logs event
def LogEvent(event):
    userManagement.LogEvent(event)


#Make sure the a given input between the given numbers are correct
def NumberInput(minNum, maxNum):
    while True:
        num = input("\nPlease enter a number ")
        try:
            val = int(num)
            if val <= maxNum and val >= minNum:
                return val
            else:
                print("Not a valid number...")
        except ValueError:
            print("Not a number...")

#Simple function that waits for user to give an input
def KeyToContinue():
    print("\nPress a key to continue...")
    input()
    os.system('cls')

#Log in screen for admins
def SystemLogIn():
    SystemLogOn = False
    while True:
        os.system("cls")
        passw = input("Please enter the system password or return0 to return to login screen ")
        global superSecretPassword
        if passw == superSecretPassword:
            SystemLogOn = True
            break
        elif passw == "return0":
            break

    if SystemLogOn:
        ShowMenuSystem()

#Log in screen for users
def LogInMenu():
    os.system('cls')
    userManagement.ReadExcelFile()
    userAmount = len(userManagement.users)
    while True:
        print("Please enter your userId")
        num = input()
        try:
            val = int(num)
            if val >= 0 and val < userAmount:
                userManagement.LogInUser(val)
                break
            else:
                print("\nNot a valid userId...")
        except ValueError:
            print("\nMust be a number...")
    return

#Logs out the user
def LogOut():
    userManagement.LogOutUser()

#Start menu for program
def StartMenu():
    while True:
        os.system('cls')
        print("1: Log into user")
        print("2: Log into system library")
        print("3: Close system")
        input = NumberInput(1, 3)
        match input:
            case 1:
                LogInMenu()
                ShowMenu()
            case 2:
                SystemLogIn()
            case 3:
                break

#Initializes of library and usermanagement singletons
def Initialize():
    global userManagement
    userManagement = UserManagement()
    global library
    library = Library()



if __name__ == '__main__':
    Initialize()
    StartMenu()