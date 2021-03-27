import tkinter as tk
from tkinter import *
from tkinter import messagebox
from matplotlib import pylab
from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt

from moneymanager import MoneyManager

win = tk.Tk()
#Set window size here to '540 x 640'
win.geometry('%sx%s' % (540, 640))
#Set the window title to 'FedUni Money Manager'
win.winfo_toplevel().title("FedUni Money Manager")
#The user number and associated variable
user_number_var = tk.StringVar()
#This is set as a default for ease of testing
user_number_var.set('')
user_number_entry = tk.Entry(win, textvariable=user_number_var,font="Calibri 16")
user_number_entry.focus_set()
#The pin number entry and associated variables
pin_number_var = tk.StringVar()
#This is set as a default for ease of testing
pin_number_var.set('')
#Modify the following to display a series of * rather than the pin ie **** not 1234
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, font="Calibri 16",show='*')
#set the user file by default to an empty string
user_file = ''
# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)
# The Entry widget to accept a numerical value to deposit or withdraw
#amount_var = tk.StringVar()
tkVar=StringVar(win)
amount_entry = tk.Entry(win)
entry_type=tk.Entry(win)
entryType = tk.StringVar()
# The transaction text widget holds text of the transactions
transaction_text_widget = tk.Text(win, height=10, width=48)
# The money manager object we will work with
user = MoneyManager()




# ---------- Button Handlers for Login Screen ----------
def clear_pin_entry(event):   
    # Clearing the pin number entry here
    pin_number_var.set('')

def handle_pin_button(event): 
    # Limiting to 4 chars in length & Set the new pin number on the pin_number_var
    NewPinAdded=event.widget['text']
    if( len ( pin_number_var.get() )<4):
        pin_number_var.set(pin_number_var.get()+NewPinAdded)

def log_in(event):
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global pin_number_var
    global user_file
    global user_num_entry

    # Creating the filename from the entered account number with '.txt' on the end
    FileName=user_number_var.get()+".txt"
    # Try to open the account file for reading
    try:
        # Open the account file for reading
        user_file = open(FileName,'r');user_file.seek(0, 0)
        # First line is account number
        user.UserNumber = read_line_from_user_file()
        if(user.UserNumber!=user_number_var.get()):
            raise Exception("Inavlid account number")
        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read 
        user.PinNumber = read_line_from_user_file()
        if(user.PinNumber!=pin_number_var.get()):
            raise Exception("Invalid pin number")
        # Reading third line for BALANCE
        user.Balance = float(read_line_from_user_file())
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        while True:          
            LineRead = read_line_from_user_file()
            LineRead.upper()
            if (LineRead=="Deposit" or LineRead=="Entertainment" or LineRead=="Food" or LineRead=="Rent" or LineRead=="Other" or LineRead=="Bills"):
                AmountLine = read_line_from_user_file()
                user.TransactionList.append((LineRead,AmountLine))
            else:
                break
        # Close the file now we're finished with it
        user_file.close()
        balance_var.set('Balance: '+str(user.Balance))
    # Catch exception for erros
    except Exception as exception_error:
        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror(" Invalid Error ",exception_error)
        user = MoneyManager()
        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        user_number_entry.focus_set()
        return
    remove_all_widgets()
    create_user_screen()

# ---------- Button Handlers for User Screen ----------
def remove_all_widgets():
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_user_file():
    global user_file
    return user_file.readline()[0:-1]

def plot_spending_graph():
    # YOUR CODE to generate the x and y lists here which will be plotted
    X=["Entertainment","Other","Rent","Food","Bills"]
    Y = [0,0,0,0,0]
    #Figure variable to be updated
    figure = Figure(figsize=(3,2), dpi=70);figure.suptitle('Spendings')
    a = figure.add_subplot(111)
    #For creating relative X and Y data
    for T in user.TransactionList:
        if(T[0]=="Entertainment"):
            Y[0]=Y[0]+float(T[1])
        if(T[0]=="Other"):
           Y[1]=Y[1]+float(T[1])
        if(T[0]=="Rent"):
            Y[2]=Y[2]+float(T[1])
        if T[0]=="Food":
            Y[3]=Y[3]+float(T[1])
        if(T[0]=="Bills"):
            Y[4]=Y[4]+float(T[1])                             
    #Your code to display the graph on the screen here - do this last
    a.plot(X, Y, marker='o')
    a.grid() 
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=5, column=0, columnspan=5, sticky='nsew')

def save_and_log_out():
    global user
    # Save the account with any new transactions
    user.save_to_file()
    # Reset the bank acount object
    user = MoneyManager()
    # Reset the account number and pin to blank
    pin_number_var.set('');user_number_var.set('');user_number_entry.focus_set()
    # Remove all widgets and display the login screen again
    remove_all_widgets();create_login_screen()

def perform_deposit():
    global user    
    global amount_entry
    global balance_label
    global balance_var
    #Increasing the account balance and append the deposit to the account file
    try:
        # Getting the cash amount to deposit & Depositing funds
        AmountT = amount_entry.get()
        TryD = user.deposit_funds(AmountT)
        if(TryD!="OK"):
            raise Exception(" Invalidation raised  ")
        #Update the transaction widget with the new transaction by calling account.get_transaction_string()   
        transaction_text_widget['state']='normal';transaction_text_widget.delete(0.0,tk.END)
        #contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.insert(tk.END,user.get_transaction_string());transaction_text_widget['state']='disabled'
        # Change the balance label to reflect the new balance
        balance_var.set('Balance($): ' + str(user.Balance))
        # Clear the amount entry
        amount_entry.delete(0,'end')
        # Update the interest graph with our new balance
        plot_spending_graph()
    except Exception as exception: #exception Handling
        return messagebox.showerror("ALERT! ",exception)  
def perform_transaction():
    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user    
    global amount_entry
    global balance_label
    global balance_var
    global entry_type
    #Decreasing the account balance and append the deposit to the account file
    try:
        # Get the cash amount to use & Get the type of entry that will be added ie rent etc    
        Check = user.add_entry(amount_entry.get(),entryType.get())
        if(Check!="OK"):
            raise Exception(Check)
        # Update the transaction widget with the new transaction by calling user.get_transaction_string()
        transaction_text_widget['state']='normal';transaction_text_widget.delete(0.0,tk.END)
        # contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.insert(tk.END,user.get_transaction_string());transaction_text_widget['state']='disabled'
        # Change the balance label to reflect the new balance
        balance_var.set('Balance : ' + str(user.Balance))
        # Clear the amount entry
        amount_entry.delete(0,'end')
        # Update the graph
        plot_spending_graph()
    except Exception as exception: #exception handling
        return messagebox.showerror("ALERT! ",exception)

   
# ---------- UI Drawing Functions ----------
def create_login_screen():  

    #  ----- Row 0 -----	
    # 'FedUni Money Manager' label here. Font size is 28.
    tk.Label(win,text="FedUni Money Manager",font="None 28").grid(row=0,column=0,columnspan=5,sticky="nsew")

    # ----- Row 1 -----
    # Acount Number / Pin label here
    tk.Label(win,text="Account Number / Pin",font="None 10").grid(row=1,column=0,sticky="nsew")
    # Account number entry here
    user_number_entry.grid(row=1,column=1)
    # Account pin entry here
    user_pin_entry.grid(row=1,column=2)

    # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    B1 = tk.Button(win,text='1');B1.bind('<Button-1>',handle_pin_button);B1.grid(row=2,column=0,sticky='nsew')
    B2 = tk.Button(win,text='2');B2.bind('<Button-1>',handle_pin_button);B2.grid(row=2,column=1,sticky='nsew')
    B3 = tk.Button(win,text='3');B3.bind('<Button-1>',handle_pin_button);B3.grid(row=2,column=2,sticky='nsew')

    # ----- Row 3 -----
    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    B4 = tk.Button(win,text='4');B4.bind('<Button-1>',handle_pin_button);B4.grid(row=3,column=0,sticky='nsew')
    B5 = tk.Button(win,text='5');B5.bind('<Button-1>',handle_pin_button);B5.grid(row=3,column=1,sticky='nsew')
    B6 = tk.Button(win,text='6');B6.bind('<Button-1>',handle_pin_button);B6.grid(row=3,column=2,sticky='nsew')

    # ----- Row 4 -----
    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    B7 = tk.Button(win,text='7');B7.bind('<Button-1>',handle_pin_button);B7.grid(row=4,column=0,sticky='nsew')
    B8 = tk.Button(win,text='8');B8.bind('<Button-1>',handle_pin_button);B8.grid(row=4,column=1,sticky='nsew')
    B9 = tk.Button(win,text='9');B9.bind('<Button-1>',handle_pin_button);B9.grid(row=4,column=2,sticky='nsew')

    # ----- Row 5 -----
    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    BC = tk.Button(win,text='Clear',activebackground='red',bg='red');BC.bind('<Button-1>',clear_pin_entry);BC.grid(row=5,column=0,sticky='nsew')
    # Button 0 here
    B0 = tk.Button(win,text='0');B0.bind('<Button-1>',handle_pin_button);B0.grid(row=5,column=1,sticky='nsew')
    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    BL = tk.Button(win,text='Login',activebackground='green',bg='green');BL.bind('<Button-1>',log_in);BL.grid(row=5,column=2,sticky='nsew')
    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(0,weight=1);win.columnconfigure(0,weight=1)
    win.rowconfigure(1,weight=1);win.columnconfigure(1,weight=1)
    win.rowconfigure(2,weight=1);win.columnconfigure(2,weight=2)
    win.rowconfigure(3,weight=1);win.columnconfigure(3,weight=2)
    win.rowconfigure(4,weight=1);win.columnconfigure(4,weight=2)
    win.rowconfigure(5,weight=1);win.columnconfigure(5,weight=2)

def create_user_screen():
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    
    # ----- Row 0 -----
    # FedUni Banking label here. Font size should be 24.
    tk.Label(win,text="FedUni Banking",font="None 24").grid(row=0,column=0,columnspan=5,sticky="nsew")

    # ----- Row 1 -----
    # Account number label here
    tk.Label(win,text="Account Number: "+user_number_var.get()).grid(row=1,column=0,sticky="nsew")
    # Balance label here
    balance_label.grid(row=1,column=1,sticky="nsew")
    # Log out button here
    tk.Button(win,text = "Log Out" ,command=save_and_log_out).grid(row=1,column=2,columnspan=2,sticky="nsew")

    # ----- Row 2 -----
    # Amount label here
    tk.Label( win,text = "Amount :" ).grid( row=2 , column=0,sticky = "nsew" )
    # Amount entry here
    amount_entry.grid( row=2 , column=1,sticky="nsew")
    # Deposit button here
    tk.Button(win,text="Deposit", command = perform_deposit ,width=11).grid(row=2, column=2,sticky="nsew")

    # ----- Row 3 -----
    # Entry type label here
    tk.Label(win,text="Entry Type : ").grid(row=3,column=0,sticky="nsew")
    # Entry drop list here
    DD = OptionMenu(win,entryType, "Food", "Rent", "Bills","Entertainment","Other")
    DD.grid(row=3,column=1,sticky="nsew")
    # Add entry button here
    tk.Button(win,text="Entry Add", command = perform_transaction ,width=11).grid(row=3, column=2,sticky="nsew")
    
    # ----- Row 4 -----
    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    
    ScrollBar=tk.Scrollbar(win)
    ScrollBar.grid(sticky="ns",columnspan=8,row=4,column=4)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    transaction_text_widget['wrap']=tk.NONE;transaction_text_widget['bd']=0;transaction_text_widget['state']='disabled'
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    transaction_text_widget['yscrollcommand']=ScrollBar.set;transaction_text_widget.grid(row=4,column=0,columnspan=8,sticky="nsew")
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    ScrollBar.config(command=transaction_text_widget.yview)#in Y directions
    transaction_text_widget['state']='normal';transaction_text_widget.delete(0.0,tk.END)
    transaction_text_widget.insert(tk.END,user.get_transaction_string());transaction_text_widget['state']='disabled'

    # ----- Row 5 - Graph -----
    # Call plot_spending_graph() here to display the graph
    plot_spending_graph()
    # ----- Set column & row weights -----
    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    
    #configuring all rows in 1 line
    win.rowconfigure(0,weight=0);win.rowconfigure(1,weight=0);win.rowconfigure(2,weight=0);win.rowconfigure(3,weight=0);win.rowconfigure(4,weight=0);win.rowconfigure(5,weight=1);
    #configuring all columns in 1 line
    win.columnconfigure(0,weight=0);win.columnconfigure(1,weight=0);win.columnconfigure(2,weight=1)
# ---------- Display Login Screen & Start Main loop ----------
create_login_screen()
win.mainloop()
