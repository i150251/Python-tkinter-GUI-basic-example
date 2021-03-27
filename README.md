# Python-tkinter-GUI-basic-example
This python code makes use of Tkinter GUI library to create a small 'Money Manager' System. This project uses Object Oriented programming technique in python.


Below is some description about each python file:


# MoneyManager.py

Consists of functions such as Add Entry, Deposit Funds, Save To File, Get Transaction string

Add Entry: Takes an amount and an item you are spending money on as input. Deducts the amount from your total available balance and adds the entry to transaction list where all transactions are stored.

Deposit funds: takes an amount as input and adds the amount to your balance.

Save to File: creates a string from all data present in transaction list where all entries are stored then prints it to a file for preserving data.

get transaction string: if user wants to view all transactions he has performed, then this function will return the transaction list.

# Main.py

This file acts as the main starting point of the program.
It consists of many GUI related functions as it makes use of Tkinter library.
It consists of MoneyManager object as it calls functions such as add entry or deposit funds.

# TestMoneyManager.py

for testing purpose. Tests functions present in MoneyManager.py file.
