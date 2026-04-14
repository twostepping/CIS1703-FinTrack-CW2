# --- Extra comments for team members ---
# could add edit/delete transactions
# go back feature
# could improve report visuals further

# domain entities: 
# base class: transaction(ID, date, amount, description)
# subclass 1: income (adds: source, isTaxable)
# subclass 2: expense (adds: category, importance level [need/want])
# subclass 3: recurringBill (adds: frequency, nextDueDate)

# functional requirements:
# transaction manager: add, view, categorise income and expenses
# smart forecasting: a function to project the user's balance for next 30 days based on current balance and recurringBill
# budget alerts: users set a budget for a cateogry, system must warn them if a new expense pushes them over
# reporting: genere a summary showing needs vs wants

import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

FILE = "data.json"



# FOR CLI
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(title="FinTrack"):
    print("=" * 50)
    print(title.center(50))
    print("=" * 50)


def pause(msg="\nPress Enter..."):
    input(msg)


def screen(title):
    clear()
    header(title)


# Classes
class Transaction():
    def __init__(self, id, date, amount, desc):
        self.__id = id
        self.__date = date
        self.__amount = amount
        self.__desc = desc

    # GETTERS
    def getID(self):
        return self.__id
    def getDate(self):
        return self.__date
    def getAmount(self):
        return self.__amount
    def getDesc(self):
        return self.__desc

    def display(self):
        return f"{self.__date:<12} £{self.__amount:<8} {self.__desc}"


class Income(Transaction):
    def __init__(self, id, date, amount, desc, source):
        super().__init__(id, date, amount, desc)
        self.__source = source

    # GETTERS
    def getSource(self):
        return self.__source

    def display(self):
        return f"[INCOME]  {super().display()} | {self.__source}"


class Expense(Transaction):
    def __init__(self, id, date, amount, desc, category, importance):
        super().__init__(id, date, amount, desc)
        self.__category = category
        self.__importance = importance

    # GETTERS
    def getCateogry(self):
        return self.__category
    def getImpotance(self):
        return self.__importance

    def display(self):
        return f"[EXPENSE] {super().display()} | {self.__category} ({self.__importance})"


class RecurringBill(Transaction):
    def __init__(self, id, date, amount, desc, frequency, nextDueDate = None):
        super().__init__(id, date, amount, desc)
        self.__frequency = frequency
        self.__nextDueDate = nextDueDate

    # GETTERS
    def getFrequency(self):
        return self.__frequency
    def getDueDate(self):
        return self.__nextDueDate
    
    def updateDueDate(self, date=None):
        if date != None:
            self.__nextDueDate = date
        else:
            self.__nextDueDate = self.__nextDueDate + timedelta(days=self.__frequency)

    def display(self):
        return f"[BILL]    {super().display()} | {self.__frequency}"



# File
def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        print("File error, starting fresh")
        return []


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# Validation
def valid_date(d):
    try:
        datetime.strptime(d, "%d/%m/%Y")
        return True
    except:
        return False


def valid_amount(amount):

    if len(amount) == 0:
        return False

    try:
        if float(amount) >= 1:
            return True
        else:
            return False
            
    except ValueError:
        return False
    

def new_id(data):
    return len(data) + 1


# System
data = load_data()



def add_income(date, amt, desc, src):

    obj = Income(new_id(data), date, round(float(amt), 2), desc, src)

    data.append({
        "type": "income",
        "id": obj._id,
        "date": obj._date,
        "amount": obj._amount,
        "desc": obj._desc,
        "source": obj.source
    })

    save_data(data)
    showMainFrame()





def add_expense(date, amt, desc, cat, imp):

    '''
    if cat == "food":
        spent = sum(x["amount"] for x in data if x.get("category") == "food")
        if spent + amt > 200:
            print("\n[-] Food budget exceeded")
            '''

    obj = Expense(new_id(data), date, round(float(amt), 2), desc, cat, imp)

    data.append({
        "type": "expense",
        "id": obj._id,
        "date": obj._date,
        "amount": obj._amount,
        "desc": obj._desc,
        "category": obj.category,
        "importance": obj.importance
    })

    save_data(data)
    showMainFrame()

'''
def add_bill():
    screen("Add Recurring Bill")

    d = input("Date (DD/MM/YYYY): ")
    if not valid_date(d):
        print("Invalid date")
        return pause()

    amt = get_amount()
    desc = input("Description: ")
    freq = input("Frequency: ")

    obj = RecurringBill(new_id(data), d, amt, desc, freq)

    data.append({
        "type": "bill",
        "id": obj._id,
        "date": obj._date,
        "amount": obj._amount,
        "desc": obj._desc,
        "frequency": obj.frequency
    })

    save_data(data)
    print("\n[+] Bill added")
    pause()
'''

def view_all():
    screen("All Transactions")

    if not data:
        print("No transactions yet")
    else:
        for x in data:
            if x["type"] == "income":
                obj = Income(x["id"], x["date"], x["amount"], x["desc"], x["source"])
            elif x["type"] == "expense":
                obj = Expense(x["id"], x["date"], x["amount"], x["desc"], x["category"], x["importance"])
            else:
                obj = RecurringBill(x["id"], x["date"], x["amount"], x["desc"], x["frequency"])

            print(obj.display())

    pause()


def forecast():
    screen("Forecast")

    balance = sum(
        x["amount"] if x["type"] == "income" else -x["amount"]
        for x in data if x["type"] in ["income", "expense"]
    )

    bills = sum(x["amount"] for x in data if x["type"] == "bill")

    print(f"Current Balance:     £{balance}")
    print(f"30 Day Prediction:   £{balance - bills}")

    pause()


def report():
    screen("Spending Report")

    needs = sum(
        x["amount"] for x in data
        if str(x.get("importance", "")).lower() == "need"
    )

    wants = sum(
        x["amount"] for x in data
        if str(x.get("importance", "")).lower() == "want"
    )

    print(f"Needs: £{needs}  " + "*" * int(needs / 10))
    print(f"Wants: £{wants}  " + "*" * int(wants / 10))

    pause()



'''
# Menu
while True:
    clear()
    header()

    options = [
        "1. Add Income",
        "2. Add Expense",
        "3. Add Bill",
        "4. View Transactions",
        "5. Forecast",
        "6. Report",
        "7. Exit"
    ]

    for o in options:
        print(o)

    print("\n" + "=" * 50)
    choice = input("Select option: ")

    if choice == "1": add_income()
    elif choice == "2": add_expense()
    elif choice == "3": add_bill()
    elif choice == "4": view_all()
    elif choice == "5": forecast()
    elif choice == "6": report()
    elif choice == "7":
        print("\nGoodbye")
        break
    else:
        print("Invalid option")
        pause()
'''
root = tk.Tk()
root.title("FinTrack")
root.geometry("420x480")

titleLabel = tk.Label(root, text="FinTrack", font=("Arial", 12))
titleLabel.pack()


# transactionFrame - decided to make the transaction history always visible, change if needed
transactionFrame = tk.Frame(root)
transactionFrame.pack()

# listbox + scrollbar
transactionListbox = tk.Listbox(transactionFrame, font=("Arial", 12))
transactionListbox.pack(side="left")
transactionScrollbar = tk.Scrollbar(transactionFrame, command=transactionListbox.yview)
transactionScrollbar.pack(side="right", fill="y")




# mainFrame - CONTAINS ALL MAIN MENU BUTTONS
mainFrame = tk.Frame(root)

# all available options
addIncomeButton = tk.Button(mainFrame, text="Add Income", font=("Arial", 12), command = lambda:showIncomeFrame())
addExpenseButton = tk.Button(mainFrame, text="Add Expense", font=("Arial", 12), command = lambda:showExpenseFrame())
reportButton = tk.Button(mainFrame, text="Generate Report", font=("Arial", 12))

# put everything on grid
addIncomeButton.grid(row=0, column=0)
addExpenseButton.grid(row=0, column=1)
reportButton.grid(row=1, column=0)





# incomeFrame - ADD INCOME
incomeFrame = tk.Frame(root)




# income amount/source/date/description
incomeEntryLabel = tk.Label(incomeFrame, text= "Income: ", font=("Arial", 12))
incomeEntry = tk.Entry(incomeFrame, font=("Arial", 12) )
incomeSourceLabel = tk.Label(incomeFrame, text="Source: ", font=("Arial", 12))
incomeSourceEntry = tk.Entry(incomeFrame, font=("Arial", 12))
incomeDateLabel = tk.Label(incomeFrame, text=f"Date: ", font=("Arial", 12))
incomeDateEntry = tk.Entry(incomeFrame, font=("Arial", 12))
incomeDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
incomeDescriptionLabel = tk.Label(incomeFrame, text="Description: ", font=("Arial", 12))
incomeDescriptionEntry = tk.Entry(incomeFrame, font=("Arial", 12))

# taxable radiobuttons
taxableOption = tk.IntVar()
taxableLabel = tk.Label (incomeFrame, text="Taxable: ", font=("Arial", 12))
taxableRadio0 = tk.Radiobutton(incomeFrame, text="Yes", font=("Arial", 12), value=1, variable=taxableOption)
taxableRadio1 = tk.Radiobutton(incomeFrame, text="No", font=("Arial", 12), value=2, variable=taxableOption)



# put everythign on grid
incomeEntryLabel.grid(row=0, column=0)
incomeEntry.grid(row=0, column=1)
incomeSourceLabel.grid(row=1, column=0)
incomeSourceEntry.grid(row=1, column=1)
incomeDateLabel.grid(row=2, column=0)
incomeDateEntry.grid(row=2, column=1)
incomeDescriptionLabel.grid(row=3, column=0)
incomeDescriptionEntry.grid(row=3, column=1)
taxableLabel.grid(row=4, column=0)
taxableRadio0.grid(row=4, column=1)
taxableRadio1.grid(row=4, column=2)




#Confirm adding income button

confirmIncomeButton = tk.Button(incomeFrame, text="Add income", font=("Arial", 12), command=lambda:add_income(datetime.now().strftime("%d/%m/%Y"), incomeEntry.get().lstrip('0'), incomeDescriptionEntry.get(), incomeSourceEntry.get()))
confirmIncomeButton.grid(row=5, column=0, columnspan=5)


# exit button
exitIncomeButton = tk.Button(incomeFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitIncomeButton.grid(row=6, column=0, columnspan=5)



# expenseFrame - ADD EXPENSES
expenseFrame = tk.Frame()

# expense amount/cateogry/date/description
expenseEntryLabel = tk.Label(expenseFrame, text="Expense cost: ", font=("Arial", 12))
expenseEntry = tk.Entry(expenseFrame, font=("Arial", 12))
categoryLabel = tk.Label(expenseFrame, text="Category:", font=("Arial", 12))
categoryEntry = tk.Entry(expenseFrame, font=("Arial", 12))
expenseDateLabel = tk.Label(expenseFrame, text=f"Date: ", font=('Arial', 12))
expenseDateEntry = tk.Entry(expenseFrame, font=("Arial", 12))
expenseDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
expenseDescriptionLabel = tk.Label(expenseFrame, text="Description: ", font=('Arial', 12))
expenseDescriptionEntry = tk.Entry(expenseFrame, font=("Arial", 12))



# importances radio buttons
importanceOption = tk.StringVar(value="Need")
importanceLabel = tk.Label(expenseFrame, text="Importance: ", font=("Arial", 12))
importanceRadio0 = tk.Radiobutton(expenseFrame, text="Need", font=("Arial", 12), value='Need', variable=importanceOption)
importanceRadio1 = tk.Radiobutton(expenseFrame, text="Want", font=("Arial", 12), value='Want', variable=importanceOption)


# put evetrything on the grid
expenseEntryLabel.grid(row=0, column=0)
expenseEntry.grid(row=0, column=1)
categoryLabel.grid(row=1, column=0)
categoryEntry.grid(row=1, column=1)
expenseDateLabel.grid(row=2, column=0)
expenseDateEntry.grid(row=2, column=1)
expenseDescriptionLabel.grid(row=3, column=0)
expenseDescriptionEntry.grid(row=3, column=1)
importanceLabel.grid(row=4, column=0)
importanceRadio0.grid(row=4, column=1)
importanceRadio1.grid(row=4, column=2)

#exit button
exitExpenseButton = tk.Button(expenseFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitExpenseButton.grid(row=6, column=0, columnspan=3)




#Confirm adding expense button
confirmExpenseButton = tk.Button(expenseFrame, text="Add expense", font=("Arial", 12), command=lambda:add_expense(datetime.now().strftime("%d/%m/%Y"), expenseEntry.get().lstrip('0'), expenseDescriptionEntry.get(), categoryEntry.get(), importanceOption.get()) )
confirmExpenseButton.grid(row=5, column=0, columnspan=3)



 # all functions to switch menus
 # could probably be combined into a single function, if we take the current frame as a parameter
def showMainFrame():
    incomeFrame.pack_forget()
    expenseFrame.pack_forget()
    mainFrame.pack()

def showIncomeFrame():
    mainFrame.pack_forget()
    incomeFrame.pack()
    
def showExpenseFrame():
    mainFrame.pack_forget()
    expenseFrame.pack()

def buttonval():
    #validates adding income
    if incomeFrame.winfo_ismapped():
        if valid_date(incomeDateEntry.get()) and valid_amount(incomeEntry.get()):
            confirmIncomeButton.config(state='active')
        else:
           confirmIncomeButton.config(state='disabled')
    #validates adding expenses
    elif expenseFrame.winfo_ismapped():
        if valid_date(expenseDateEntry.get()) and valid_amount(expenseEntry.get()):
            confirmExpenseButton.config(state='active')
        else:
            confirmExpenseButton.config(state='disabled')
  


    root.after(10, buttonval)

buttonval()
showMainFrame()


root.mainloop()
