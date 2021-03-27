import tkinter as tk
from tkinter import *
class MoneyManager():

       
    def __init__(self):
        self.UserNumber = ''
        self.PinNumber = ''
        self.Balance = ''
        self.TransactionList=[]

    def add_entry(self, amount, entry_type):
        try:
            if(self.Balance>=float(amount)):
                self.Balance=round(self.Balance-float(amount),4)
                if(entry_type=="Entertainment" or entry_type=="Bills" or entry_type=="Other" or entry_type=="Food"  or entry_type=="Rent"):
                    self.TransactionList.append((entry_type,float(amount)))
                    return "OK"
                else:
                    return "Entry Err"
                return "OK"
            else:
                return "NO BAL ERROR"
        except ValueError:
            return "Value Error exception"
        except TypeError:
            return "Type Error exception"

    def deposit_funds(self, amount):
        try:
            if(float(amount)>0.0):
                self.Balance=round(self.Balance+float(amount),4)
                self.TransactionList.append(("Deposit",float(amount)))
                return "OK"
            else:
                return " VALUE ERROR"
        except ValueError:
            return "Value Error exception"
        except TypeError:
            return "Type Error exception"

    def save_to_file(self):    
        FILE=str(self.UserNumber)+".txt"
        DATA = str(self.UserNumber)+"\n"
        DATA += str(self.PinNumber)+"\n"
        DATA += str(self.Balance)+"\n"
        DATA += str(self.get_transaction_string())
        with open(FILE,'w') as w:
            w.write(DATA)
        

    def get_transaction_string(self):
        TR=""
        for T in self.TransactionList:
            TR = TR + str ( T[0] ) + "\n" + str ( T[1] )+"\n"     
        return  TR
    


        



        
