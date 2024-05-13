from faker import Faker
import pandas as pd
fake = Faker()
import ast



class generateUsers:
    def __init__(self):
        n = 100
        names = []
        adresses = []
        for i in range(n):
            names.append(fake.name())
            adresses.append(fake.address())
            
        #print(names, adresses)

        users = pd.DataFrame()
        users['NAME'] = names
        users['ADDRESS'] = adresses
        users['BORROWEDBOOKS'] = [[] for _ in range(len(users))]
        users['RESERVATIONS'] = [[] for _ in range(len(users))]
        users['LOG'] = [[] for _ in range(len(users))]
        users['INBOX'] = [[] for _ in range(len(users))]
        
        #print(users)
        users.to_excel('user_data.xlsx',index=False)
        
    userDF = pd.read_excel('user_data.xlsx')

DFuser = generateUsers().userDF
print(DFuser.head())
        
print(type(ast.literal_eval(DFuser['INBOX'][0])))
print(ast.literal_eval(DFuser['INBOX'][0]))
#print(ast.literal_eval(DFuser['INBOX']))
        
        
        