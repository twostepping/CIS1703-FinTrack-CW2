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
# reporting: generate a summary showing needs vs wants for the user

#==============================================================================================
#Importing all necessary modules, including json for file handling, os for clearing the console, datetime for handling dates, and tkinter for the GUI.
#==============================================================================================
import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

FILE = "data.json"

#==============================================================================================
#Utility functions for the CLI version of the application, including functions to clear the console, display headers, pause for user input, and manage screen transitions.
#==============================================================================================

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

#==============================================================================================
#Class definitions
#==============================================================================================
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
    def __init__(self, id, date, amount, desc, source, taxable):
        super().__init__(id, date, amount, desc)
        self.__source = source
        self.__taxable = taxable

    # GETTERS
    def getSource(self):
        return self.__source
    def getTaxable(self):
        return self.__taxable

    def display(self):
        return f"[INCOME]  {super().display()} | {self.__source}"


class Expense(Transaction):
    def __init__(self, id, date, amount, desc, category, importance):
        super().__init__(id, date, amount, desc)
        self.__category = category
        self.__importance = importance

    # GETTERS
    def getCategory(self):
        return self.__category
    def getImportance(self):
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


#==============================================================================================
# File handling and validation functions. These functions manage loading and saving data to a JSON file, as well as validating user input for dates, amounts, and text fields.
#==============================================================================================

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
    
def valid_text(text): # used for bill desc, income/exp source
    if len(text.strip()) == 0:
        return False
    return True

def valid_num(num): # used for frequency
    try:
        int(num) # generates valueerror if num is not an integer or if it is blank
        return True
    except ValueError:
        return False
    

def new_id(data):
    return len(data) + 1

#==============================================================================================
# System functions: these functions implement the core functionality of the application, including adding income, expenses, and bills, viewing transactions, forecasting, and generating reports.
#==============================================================================================
data = load_data()



def add_income(date, amt, desc, src, taxable):

    obj = Income(new_id(data), date, round(float(amt), 2), desc, src, taxable)

    data.append({
        "type": "income",
        "id": obj.getID(),
        "date": obj.getDate(),
        "amount": obj.getAmount(),
        "desc": obj.getDesc(),
        "source": obj.getSource(),
        "taxable": obj.getTaxable()
    })
    
    transactionListbox.insert("end", f"income - {obj.getDate()} - £{obj.getAmount()} from {obj.getSource()} - {obj.getDesc()} - {obj.getTaxable()}")

    save_data(data)





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
        "id": obj.getID(),
        "date": obj.getDate(),
        "amount": obj.getAmount(),
        "desc": obj.getDesc(),
        "category": obj.getCategory(),
        "importance": obj.getImportance()
    })
    
    transactionListbox.insert("end", f"expense - {obj.getDate()} - £{obj.getAmount()} from {obj.getCategory()} - {obj.getDesc()} - {obj.getImportance()}")

    save_data(data)

def add_bill(date, amt, desc, freq):
    
    obj = RecurringBill(new_id(data), date, round(float(amt), 2), desc, freq)
    
    data.append({
        "type": "bill",
        "id": obj.getID(),
        "date": obj.getDate(),
        "amount": obj.getAmount(),
        "desc": obj.getDesc(),
        "frequency": obj.getFrequency()
    })
    
    transactionListbox.insert("end", f"bill - {obj.getDate()} - £{obj.getAmount()} from {obj.getDesc()} - every {obj.getFrequency()} days")
    
    save_data(data)

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
                obj = Income(x["id"], x["date"], x["amount"], x["desc"], x["source"], x["taxable"])
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
# we need an x scroll bar, current one gets put into the wrong place
transactionListbox = tk.Listbox(transactionFrame, font=("Arial", 12), width = 40) # width is measured in charcters, not pixels for some reason
transactionListbox.pack(side="left")
#transactionScrollbarX = tk.Scrollbar(transactionFrame, command=transactionListbox.xview, orient="horizontal")
transactionScrollbarY = tk.Scrollbar(transactionFrame, command=transactionListbox.yview)
#transactionScrollbarX.pack(side="bottom",fill="y")
transactionScrollbarY.pack(side="right", fill="y")

# add all existing data to the listbox
for item in data:
    if item['type'] == "income":
        transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['source']} - {item['desc']} - {item['taxable']}")
    elif item['type'] == "expense":
        transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['category']} - {item['desc']} - {item['importance']}")
    elif item['type'] == "bill":
        transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['desc']} - every {item['frequency']} days")

# mainFrame - CONTAINS ALL MAIN MENU BUTTONS
mainFrame = tk.Frame(root)

# all available options
addIncomeButton = tk.Button(mainFrame, text="Add Income",height=2,width=15, font=("Arial", 12), command = lambda:showIncomeFrame())
addExpenseButton = tk.Button(mainFrame, text="Add Expense", height=2, width=15, font=("Arial", 12), command = lambda:showExpenseFrame())
addRecurringBill = tk.Button(mainFrame, text="Add Bill", height=2, width=15, font=("Arial", 12), command = lambda:showBillFrame())
reportButton = tk.Button(mainFrame, text="Generate Report", height=2, width=15, font=("Arial", 12), command=lambda:showReportFrame())

# put everything on grid
addIncomeButton.grid(row=0, column=0)
addExpenseButton.grid(row=0, column=1)
addRecurringBill.grid(row=1, column=0)
reportButton.grid(row=1, column=1)





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

incomeWarningLabel = tk.Label(incomeFrame, text="", font=("Arial", 12))

# taxable radiobuttons
taxableOption = tk.StringVar(value="taxable")
taxableLabel = tk.Label (incomeFrame, text="Taxable: ", font=("Arial", 12))
taxableRadio0 = tk.Radiobutton(incomeFrame, text="Yes", font=("Arial", 12), value="taxable", variable=taxableOption)
taxableRadio1 = tk.Radiobutton(incomeFrame, text="No", font=("Arial", 12), value="not taxable", variable=taxableOption)

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

incomeWarningLabel.grid(row=5, column=0, columnspan=3)

#Confirm adding income button
confirmIncomeButton = tk.Button(incomeFrame, text="Add income", font=("Arial", 12), command=lambda:add_income(datetime.now().strftime("%d/%m/%Y"), incomeEntry.get().lstrip('0'), incomeDescriptionEntry.get(), incomeSourceEntry.get(), taxableOption.get()))
confirmIncomeButton.grid(row=6, column=0, columnspan=5)

# exit button 
exitIncomeButton = tk.Button(incomeFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitIncomeButton.grid(row=7, column=0, columnspan=5)





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

expenseWarningLabel = tk.Label(expenseFrame, text="", font=("Arial", 12))

# importances radio buttons
importanceOption = tk.StringVar(value="need")
importanceLabel = tk.Label(expenseFrame, text="Importance: ", font=("Arial", 12))
importanceRadio0 = tk.Radiobutton(expenseFrame, text="Need", font=("Arial", 12), value='need', variable=importanceOption)
importanceRadio1 = tk.Radiobutton(expenseFrame, text="Want", font=("Arial", 12), value='want', variable=importanceOption)

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

expenseWarningLabel.grid(row=5, column=0, columnspan=3)

#Confirm adding expense button
confirmExpenseButton = tk.Button(expenseFrame, text="Add expense", font=("Arial", 12), command=lambda:add_expense(datetime.now().strftime("%d/%m/%Y"), expenseEntry.get().lstrip('0'), expenseDescriptionEntry.get(), categoryEntry.get(), importanceOption.get()) )
confirmExpenseButton.grid(row=6, column=0, columnspan=3)

#exit button
exitExpenseButton = tk.Button(expenseFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitExpenseButton.grid(row=7, column=0, columnspan=3)





# billFrame - lets you add/cancel recurring bills
billFrame = tk.Frame(root)

# bill amount/desc/frequency/date
billAmountLabel = tk.Label(billFrame, text="Amount: ", font=("Arial", 12))
billAmountEntry = tk.Entry(billFrame, font=("Arial", 12))
billDescriptionLabel = tk.Label(billFrame, text="Description: ", font=("Arial", 12))
billDescriptionEntry = tk.Entry(billFrame, font=("Arial", 12))
billDateLabel = tk.Label(billFrame, text=f"Date: ", font=('Arial', 12))
billDateEntry = tk.Entry(billFrame, font=("Arial", 12))
billDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
billFrequencyLabel = tk.Label(billFrame, text="Frequency (days): ", font=("Arial", 12))
billFrequencyEntry = tk.Entry(billFrame, font=("Arial", 12))
billDueDateButton = tk.Button(billFrame, text="Calculate Due Date ", font=("Arial", 12), command=lambda: calculateDueDate())
billDueDateLabel = tk.Label(billFrame, font=("Arial", 12))

billWarningLabel = tk.Label(billFrame, text="", font=("Arial", 12))

# calculate due date
def calculateDueDate():
    if len(billFrequencyEntry.get().strip()) != 0:
        billDueDateLabel.config(text=f"{(datetime.strptime(billDateEntry.get(), "%d/%m/%Y") + timedelta(days=int(billFrequencyEntry.get()))).strftime("%d/%m/%Y")}")

#put everything on the grid
billAmountLabel.grid(row=0, column=0)
billAmountEntry.grid(row=0, column=1)
billDescriptionLabel.grid(row=1, column=0)
billDescriptionEntry.grid(row=1, column=1)
billDateLabel.grid(row=2, column=0)
billDateEntry.grid(row=2, column=1)
billFrequencyLabel.grid(row=3, column=0)
billFrequencyEntry.grid(row=3, column=1)
billDueDateButton.grid(row=4, column=0)
billDueDateLabel.grid(row=4, column=1)

billWarningLabel.grid(row=5, column=0, columnspan=3)

#confirm adding bill button
confirmBillButton = tk.Button(billFrame, text="Add Recurring Bill", font=("Arial", 12), command=lambda:add_bill(datetime.now().strftime("%d/%m/%Y"), billAmountEntry.get().lstrip('0'), billDescriptionEntry.get(), billFrequencyEntry.get()))
confirmBillButton.grid(row=6, column=0, columnspan=3)

#exit button
exitBillButton = tk.Button(billFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitBillButton.grid(row=7, column=0, columnspan=2)





# reportFrame - lets you do smart forecasting, generate reports, budget alerts
reportFrame = tk.Frame(root)

# generate report, smart forecasting, budget alerts
generateReportButton = tk.Button(reportFrame, text="Generate Report", font=("Arial", 12))
smartForecastingButton = tk.Button(reportFrame, text="Smart forecast", font=("Arial", 12))
showBudgetAlertButton = tk.Button(reportFrame, text="Show Budget Alerts", font=("Arial", 12))

reportLabel = tk.Label(reportFrame, text="", font=("Arial", 12))

# put everything on grid
generateReportButton.grid(row=0, column=0)
smartForecastingButton.grid(row=0, column=1)
showBudgetAlertButton.grid(row=0, column=2)

reportLabel.grid(row=1, column=0, columnspan=3)

#exit button
exitReportButton = tk.Button(reportFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitReportButton.grid(row=2, column=0, columnspan=3)





 # all functions to switch menus
 # could probably be combined into a single function, if we take the current frame as a parameter
def showMainFrame():
    incomeFrame.pack_forget()
    expenseFrame.pack_forget()
    billFrame.pack_forget()
    reportFrame.pack_forget()
    mainFrame.pack()

def showIncomeFrame():
    mainFrame.pack_forget()
    incomeFrame.pack()
    
def showExpenseFrame():
    mainFrame.pack_forget()
    expenseFrame.pack()

def showBillFrame():
    mainFrame.pack_forget()
    billFrame.pack()
    
def showReportFrame():
    mainFrame.pack_forget()
    reportFrame.pack()

def buttonval():
    #validates adding income
    if incomeFrame.winfo_ismapped():
        if valid_date(incomeDateEntry.get()) and valid_amount(incomeEntry.get()) and valid_text(incomeSourceEntry.get()):
            confirmIncomeButton.config(state='active')
            incomeWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
        else:
            confirmIncomeButton.config(state='disabled')
            incomeWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")

    #validates adding expenses
    elif expenseFrame.winfo_ismapped():
        if valid_date(expenseDateEntry.get()) and valid_amount(expenseEntry.get()) and valid_text(categoryEntry.get()):
            confirmExpenseButton.config(state='active')
            expenseWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
        else:
            confirmExpenseButton.config(state='disabled')
            expenseWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
            
    elif billFrame.winfo_ismapped():
        if valid_date(billDateEntry.get()) and valid_amount(billAmountEntry.get()) and valid_num(billFrequencyEntry.get()) and valid_text(billDescriptionEntry.get()):
            confirmBillButton.config(state='active')
            billWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
        else:
            confirmBillButton.config(state='disabled')
            billWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
  
    root.after(10, buttonval)

buttonval()
showMainFrame()

root.mainloop()
