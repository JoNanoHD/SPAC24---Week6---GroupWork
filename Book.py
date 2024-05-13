#DEPRECATED AF
class Book:
    #Switches availability of book
    def ChangeAvailableStatus(df):
        df["AVAILABLE"] = not df["AVAILABLE"]

    #Adds the given log to the books logs
    def AddLog(df, log):
        df["LOG"].append(log)

    #Adds the specified user id to the reservations
    def AddReservation(df, userId):
        df["RESERVATIONS"].append(userId)

    #Removes either the first reservation on the book or the reservation for the given user id
    def RemoveReservation(df, userId = -1):
        if id == -1:
            df["RESERVATIONS"].pop(0)
        else:
            df["RESERVATIONS"].remove(userId)

    #Checks whether the book is reserved
    def NotReserved(df):
        return not df["RESERVATIONS"]