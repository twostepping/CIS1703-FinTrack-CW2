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

# corrected attribute access to match single underscore naming convention
# previously used __ which does not exist and causes attribute errors

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
#Class definitions
#==============================================================================================
# don't use __, it involves name mangling which makes inheritance really annoying, _ is already private attributes by itself

class Transaction():
    def __init__(self, id, date, amount, desc):
        self._id = id
        self._date = date
        self._amount = amount
        self._desc = desc

    # GETTERS
    def getID(self):
        return self._id
    def getDate(self):
        return self._date
    def getAmount(self):
        return self._amount
    def getDesc(self):
        return self._desc
    
    def addItem(self, type):
        # add to the data.json
        data.append({
            "type": type,
            "id": self._id,
            "date": self._date,
            "amount":self._amount,
            "desc": self._desc
        })

        # add to the end of the listbox
        transactionListbox.insert("end", f"{type} - {self._date} - £{self._amount} for {self._desc}")
        updateBudgetProgress() # update the budget progress bar
    
        save_data(data)
        


class Income(Transaction):
    def __init__(self, id, date, amount, desc, source, taxable):
        super().__init__(id, date, amount, desc)
        self._source = source
        self._taxable = taxable

    # GETTERS
    def getCategory(self):
        return self._category

    def getImportance(self):
        return self._importance
    
    def addItem(self):
        # clears all the entrys
        incomeEntry.delete(0, tk.END)
        incomeSourceEntry.delete(0, tk.END)
        incomeDateEntry.delete(0, tk.END)
        incomeDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        incomeDescriptionEntry.delete(0, tk.END)
        
        incomeEntry.focus_set() # returns focus to the first entry, the income entry
    
        # adds item to data
        data.append({
            "type": "income",
            "id": self._id,
            "date": self._date,
            "amount": self._amount,
            "desc": self._desc,
            "source": self._source,
            "taxable": self._taxable
        })
        
        
        save_data(data) # saves
    
        transactionListbox.insert("end", f"income - {self._date} - £{self._amount} from {self._source} - {self._desc} - {self._taxable}") # adds to the listbox


class Expense(Transaction):
    def __init__(self, id, date, amount, desc, category, importance):
        super().__init__(id, date, amount, desc)
        self._category = category
        self._importance = importance

    # GETTERS
    def getCategory(self):
        return self.__category
    def getImportance(self):
        return self.__importance
    
    def addItem(self):
        total = 0 # used for the budget alert
        
        expenseEntry.delete(0, tk.END)
        expenseCategoryEntry.delete(0, tk.END)
        expenseDateEntry.delete(0, tk.END)
        expenseDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        expenseDescriptionEntry.delete(0, tk.END)
        
        expenseEntry.focus_set()
    
        # budget alert
        for budget in data: # finds the correct budget
            if budget['type'] == "budget" and budget["desc"] == self._category:
                for item in data: # sums all expenses for that budget
                    if item["type"] == "expense" and item["category"] == self._category:
                        total += item["amount"]
            
                if total + float(self._amount) > budget["amount"]: # if over budget, alert the user
                    if tk.messagebox.askyesno("Budget Alert", f"Adding this expense will put you {(total+float(self._amount)-budget["amount"])} over your budget for {self._category}. \nDo you still want to add this expense?") == False:
                        return False
    
        data.append({
            "type": "expense",
            "id": self._id,
            "date": self._date,
            "amount": self._amount,
            "desc": self._desc,
            "category": self._category,
            "importance": self._importance
        })
        save_data(data)
    
        transactionListbox.insert("end", f"expense - {self._date} - £{self._amount} from {self._category} - {self._desc} - {self._importance}")




class RecurringBill(Transaction):
    def __init__(self, id, date, amount, desc, frequency, nextDueDate = None):
        super().__init__(id, date, amount, desc)
        self._frequency = frequency

    # GETTERS 
    def getFrequency(self):
        return self._frequency
    
    def addItem(self):
        billAmountEntry.delete(0, tk.END)
        billDescriptionEntry.delete(0, tk.END)
        billDateEntry.delete(0, tk.END)
        billDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        billFrequencyEntry.delete(0, tk.END)
        billDueDateLabel.config(text="")
        
        billAmountEntry.focus_set()
    
    
        data.append({
            "type": "bill",
            "id": self._id,
            "date": self._date,
            "amount": self._amount,
            "desc": self._desc,
            "frequency": self._frequency
        })
    
        transactionListbox.insert("end", f"bill - {self._date} - £{self._amount} from {self._desc} - every {self._frequency} days")
    
        save_data(data)

    
class Budget(Transaction):
    def __init__(self, id, date, amount, desc):
        super().__init__(id, date, amount, desc)
        
    def addItem(self):
        # these clear the entrys on the budget frame, so that the user doesn't have to do it themself
        budgetAmountEntry.delete(0, tk.END)
        budgetCategoryEntry.delete(0, tk.END)
        budgetDateEntry.delete(0, tk.END)
        budgetDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        
        budgetAmountEntry.focus_set()
    
        # add to the data.json
        data.append({
            "type": "budget",
            "id": self._id,
            "date": self._date,
            "amount":self._amount,
            "desc": self._desc
        })

        # add to the end of the listbox
        transactionListbox.insert("end", f"budget - {self._date} - £{self._amount} for {self._desc}")
        updateBudgetProgress() # update the budget progress bar
    
        save_data(data)

#==============================================================================================
# File handling and validation functions. These functions manage loading and saving data to a JSON file, as well as validating user input for dates, amounts, and text fields.
#==============================================================================================

def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
            
    except json.JSONDecodeError:
    messagebox.showwarning("Data Error", "Data file corrupted. Starting fresh.")
    return []


def save_data(data):
    
    # This makes sure that the item IDs are all in order, and not by sorting them
    # IDs are created based on order of creation, and that order should never change so there's no need to sort them
    # instead, the IDs are changed such that they are in order
    
    ID1 = -1 # previous ID
    for item in data:
        if ID1 == -1: # skips the first item since that means there is no previous item to compare against
            ID1 = 1
            item["id"] = 1 # makes sure first item has ID 1
            continue # skips the rest of the code for this loop

        if ID1+1 != item["id"]: # if the ID isn't 1 greater than previous ID, update it
            item["id"] = ID1+1
    
        ID1 = item["id"] # update data
    
    # overwrites existing data with the new data
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)
        

def delete_transaction(): 
    index = transactionListbox.curselection()
    increment = 0
    
    if not index: # checks to make sure something is selected
        return False
    
    if tk.messagebox.askyesno("Confirmation", f"Are you sure you want to delete this item?") == False:
        return False
    
    # every time data is saved, it automatically fixes any unordered ids
    # so the ID of the item in the listbox should match the item ID
    
    # need to differentiate between the budget frame and not budget frame
    # because this index only takes in account the items being displayed, which is different on the budget frame
    # so items in data.json, after budget items, will have a difference of x between ID and listbox index, where x is the number of budgets before it
    
    if budgetFrame.winfo_ismapped():
        for item in data:
            if item["type"] != "budget":
                increment += 1
            if (item["id"] == int(index[0])+1+increment): # +1 because id indexing starts at 1
                data.remove(item)
                save_data(data)
                updateBudgetProgress()
                break
        
    else:
        for item in data:
            if item["type"] == "budget":
                increment += 1
            if (item["id"] == int(index[0])+1+increment):
                data.remove(item)
                save_data(data)
                break

    transactionListbox.delete(tk.ANCHOR)


#==============================================================================================
# Validations - prevents the add item buttons being pressed until all requires entrys are valid
#==============================================================================================
def valid_date(d):
    try:
        datetime.strptime(d, "%d/%m/%Y")
        return True
    except:
        return False


def valid_amount(amount):
    if len(amount) == 0: # check if the value exists
        return False

    try:
        if float(amount) > 0: # can't enter negatives because there's no reason to? negative expenditure is just income and negative income is just expenditure
            return True
        else:
            return False
            
    except ValueError: # happens when it's not a number
        return False
    
    
def valid_text(text): # used for bill desc, income/exp source
    if len(text.strip()) == 0:
        return False
    return True


def valid_num(num): # used for frequency
    try:
        if int(num) > 0: # generates valueerror if num is not an integer or if it is blank
            return True
        else: # can't have negative frequency
            return False
    
    except ValueError:
        return False
    

def new_id(data):
    return len(data) + 1


#==============================================================================================
# System functions: these functions implement the core functionality of the application, including adding income, expenses, and bills, viewing transactions, forecasting, and generating reports.
#==============================================================================================
data = load_data()

# all items in the data.json are converted into objects
for item in data:
    if item["type"] == "income":
        obj = Income(item["id"], item["date"], item["amount"], item["desc"], item["source"], item["taxable"])
    elif item["type"] == "expense":
        obj = Expense(item["id"], item["date"], item["amount"], item["desc"], item["category"], item["importance"])
    elif item["type"] == "bill":
        obj = RecurringBill(item["id"], item["date"], item["amount"], item["desc"], item["frequency"])
    elif item["type"] == "budget":
        obj = Budget(item["id"], item["date"], item["amount"], item["desc"])


def add_income(date, amt, desc, src, taxable):
    obj = Income(new_id(data), date, round(float(amt), 2), desc, src, taxable)
    obj.addItem()


def add_expense(date, amt, desc, cat, imp):
    obj = Expense(new_id(data), date, round(float(amt), 2), desc, cat, imp)
    obj.addItem()


def add_bill(date, amt, desc, freq):
    obj = RecurringBill(new_id(data), date, round(float(amt), 2), desc, freq)
    obj.addItem()
    
    
def add_budget(date, amt, cat):
    obj = Budget(new_id(data), date, round(float(amt), 2), desc=cat) # using desc as category, we can visually differentiate for the user
    obj.addItem()
    
    

def generateForecast():
    bills = 0
    
    balance = sum( # find the total balance by adding all the income and subtracting all the expenses
        x["amount"] if x["type"] == "income" else -x["amount"]
        for x in data if x["type"] in ["income", "expense"]
    )

    bills = 0
for x in data:
    if x["type"] == "bill":
        try:
            freq = int(x["frequency"])
            if freq > 0:
                bills += x["amount"] * (30 // freq)
        except:
            continue      # finds all the bills and multiply amount paid by how many days you'll pay in the 30 days.

    reportLabel.config(text=f"Balance: £{balance} \n30 Day Prediction: £{balance-bills}") # show the user


def generateReport():
    needs = sum( # sum all the amount spent for needs
        x["amount"] for x in data
        if str(x.get("importance", "")).lower() == "need"
    )

    wants = sum( # sum all the amount spent for wants
        x["amount"] for x in data
        if str(x.get("importance", "")).lower() == "want"
    )
    
    reportLabel.config(text=f"Needs: £{needs}\n Wants: £{wants}") # present to user
    

def budgetReport():
    totals = [[], [], []] # category - budget - amount spent
    index = -1 # immediatly gets incremented to 0
    budgetMsg = ""
    
    for budget in data: # this definitely could be simplifed, but it works
        if budget['type'] == "budget": # find each budget
            totals[0].append(budget['desc'])   # create a new cell for the found budget
            totals[1].append(budget['amount']) # create a new cell for the budgets amount
            totals[2].append(0)                # create a new cell for the amount spent towards that budget
            index += 1 # update index to select current budget in the totals[] data structure
            for item in data:
                if item['type'] == 'expense': # find expense with the correct category
                    if item['category'] == budget['desc']:
                        (totals[2])[index] += int(item['amount']) # add the amount spent to the total
                        
    for i in range (len(totals[0])):
        amount = totals[2][i] - totals[1][i] # amount - budget > 0 means over budget (400 spent - 200 budget = -200 (200 overbudget))
        
        if i > 0: # putting \n at the start of each msg also works, but the entire msg is started on a new line
            budgetMsg = budgetMsg + "\n"
        
        if amount == 0: # update the presented msg
            budgetMsg = budgetMsg + f"{totals[0][i]} - £{amount} remaining"
        elif amount > 0:
            budgetMsg = budgetMsg + f"{totals[0][i]} - £{amount} over budget"
        else:
            budgetMsg = budgetMsg + f"{totals[0][i]} - £{-amount} remaining"
            
    reportLabel.config(text=budgetMsg)
    




#==============================================================================================
# TKINTER GUI - Contains the initial setup for the GUI, as well as all the frames, buttons, entrys, etc
#==============================================================================================
root = tk.Tk()
root.title("FinTrack")
root.geometry("420x480")

titleLabel = tk.Label(root, text="FinTrack", font=("Arial", 12))
titleLabel.pack()





# transactionFrame - decided to make the transaction history always visible, change if needed
transactionFrame = tk.Frame(root)
transactionFrame.pack()

# listbox + scrollbar  
# we need an X axis scroll bar, current one gets put into the wrong place
transactionListbox = tk.Listbox(transactionFrame, font=("Arial", 12), width = 40) # width is measured in charcters, not pixels for some reason
transactionListbox.pack(side="left")
#transactionScrollbarX = tk.Scrollbar(transactionFrame, command=transactionListbox.xview, orient="horizontal")
transactionScrollbarY = tk.Scrollbar(transactionFrame, command=transactionListbox.yview)
#transactionScrollbarX.pack(side="bottom",fill="y")
transactionScrollbarY.pack(side="right", fill="y")


# add all existing data to the listbox
def loadListbox():
    for item in data:
        if item['type'] == "income":
            transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['source']} - {item['desc']} - {item['taxable']}")
        elif item['type'] == "expense":
            transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['category']} - {item['desc']} - {item['importance']}")
        elif item['type'] == "bill":
            transactionListbox.insert("end", f"{item['type']} - {item['date']} - £{item['amount']} from {item['desc']} - every {item['frequency']} days")
loadListbox()





# mainFrame - CONTAINS ALL MAIN MENU BUTTONS
mainFrame = tk.Frame(root)

# all available options
addIncomeButton = tk.Button(mainFrame, text="Add Income",height=2,width=15, font=("Arial", 12), command = lambda:showIncomeFrame())
addExpenseButton = tk.Button(mainFrame, text="Add Expense", height=2, width=15, font=("Arial", 12), command = lambda:showExpenseFrame())
addRecurringBill = tk.Button(mainFrame, text="Add Bill", height=2, width=15, font=("Arial", 12), command = lambda:showBillFrame())
budgettingButton = tk.Button(mainFrame, text="Budgetting", height=2, width=15, font=("Arial", 12), command=lambda:showBudgetFrame())
reportButton = tk.Button(mainFrame, text="Generate Report", height=2, width=15, font=("Arial", 12), command=lambda:showReportFrame())


# put everything on grid
addIncomeButton.grid(row=0, column=0)
addExpenseButton.grid(row=0, column=1)
addRecurringBill.grid(row=1, column=0)
budgettingButton.grid(row=1, column=1)
reportButton.grid(row=2, column=0, columnspan=2)





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
confirmIncomeButton.grid(row=6, column=0, columnspan=3)
# delete button
deleteIncomeButton = tk.Button(incomeFrame, text="Delete Selected", font=("Arial",12), command=lambda: delete_transaction())
deleteIncomeButton.grid(row=7, column=0, columnspan=3)

# exit button 
exitIncomeButton = tk.Button(incomeFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitIncomeButton.grid(row=8, column=0, columnspan=3)





# expenseFrame - ADD EXPENSES
expenseFrame = tk.Frame()

# expense amount/cateogry/date/description
expenseEntryLabel = tk.Label(expenseFrame, text="Expense cost: ", font=("Arial", 12))
expenseEntry = tk.Entry(expenseFrame, font=("Arial", 12))
expenseCategoryLabel = tk.Label(expenseFrame, text="Category:", font=("Arial", 12))
expenseCategoryEntry = tk.Entry(expenseFrame, font=("Arial", 12))
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
expenseCategoryLabel.grid(row=1, column=0)
expenseCategoryEntry.grid(row=1, column=1)
expenseDateLabel.grid(row=2, column=0)
expenseDateEntry.grid(row=2, column=1)
expenseDescriptionLabel.grid(row=3, column=0)
expenseDescriptionEntry.grid(row=3, column=1)
importanceLabel.grid(row=4, column=0)
importanceRadio0.grid(row=4, column=1)
importanceRadio1.grid(row=4, column=2)

expenseWarningLabel.grid(row=5, column=0, columnspan=3)

#Confirm adding expense button
confirmExpenseButton = tk.Button(expenseFrame, text="Add expense", font=("Arial", 12), command=lambda:add_expense(datetime.now().strftime("%d/%m/%Y"), expenseEntry.get().lstrip('0'), expenseDescriptionEntry.get(), expenseCategoryEntry.get(), importanceOption.get()) )
confirmExpenseButton.grid(row=6, column=0, columnspan=3)
# delete button
deleteExpenseButton = tk.Button(expenseFrame, text="Delete Selected", font=("Arial",12), command=lambda: delete_transaction())
deleteExpenseButton.grid(row=7, column=0, columnspan=3)

#exit button
exitExpenseButton = tk.Button(expenseFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitExpenseButton.grid(row=8, column=0, columnspan=3)





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

billWarningLabel.grid(row=5, column=0, columnspan=2)

#confirm adding bill button
confirmBillButton = tk.Button(billFrame, text="Add Recurring Bill", font=("Arial", 12), command=lambda:add_bill(datetime.now().strftime("%d/%m/%Y"), billAmountEntry.get().lstrip('0'), billDescriptionEntry.get(), billFrequencyEntry.get()))
confirmBillButton.grid(row=6, column=0, columnspan=2)
# delete button
deleteBillButton = tk.Button(billFrame, text="Delete Selected", font=("Arial",12), command=lambda: delete_transaction())
deleteBillButton.grid(row=7, column=0, columnspan=2)

#exit button
exitBillButton = tk.Button(billFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitBillButton.grid(row=8, column=0, columnspan=2)





#budgetFrame - lets you set a budget
budgetFrame = tk.Frame(root)

# add budget amount, category, etc
budgetAmountLabel = tk.Label(budgetFrame, text="Amount: ", font=("Arial, 12"))
budgetAmountEntry = tk.Entry(budgetFrame, font=("Arial", 12))
budgetCategoryLabel = tk.Label(budgetFrame, text="Category:", font=("Arial", 12))
budgetCategoryEntry = tk.Entry(budgetFrame, font=("Arial", 12))
budgetDateLabel = tk.Label(budgetFrame, text=f"Date: ", font=("Arial", 12))
budgetDateEntry = tk.Entry(budgetFrame, font=("Arial", 12))
budgetDateEntry.insert(0, datetime.now().strftime("%d/%m/%Y"))

budgetWarningLabel = tk.Label(budgetFrame, text="", font=("Arial", 12))

#put everything on the grid
budgetAmountLabel.grid(row=0, column=0)
budgetAmountEntry.grid(row=0, column=1)
budgetCategoryLabel.grid(row=1, column=0)
budgetCategoryEntry.grid(row=1, column=1)
budgetDateLabel.grid(row=2, column=0)
budgetDateEntry.grid(row=2, column=1)

budgetWarningLabel.grid(row=4, column=0, columnspan=2)

# add budget
confirmBudgetButton = tk.Button(budgetFrame, text="Add Budget", font=("Arial", 12), command=lambda:add_budget(datetime.now().strftime("%d/%m/%Y"), budgetAmountEntry.get(), budgetCategoryEntry.get()))
confirmBudgetButton.grid(row=6, column=0, columnspan=2)
# delete button
deleteBudgetButton = tk.Button(budgetFrame, text="Delete Selected", font=("Arial",12), command=lambda: delete_transaction())
deleteBudgetButton.grid(row=7, column=0, columnspan=2)


#exit button
exitBudgetButton = tk.Button(budgetFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitBudgetButton.grid(row=8, column=0, columnspan=2)



# budget progress frame, gets shown below the notice label
budgetProgressFrame = tk.Frame(budgetFrame)
budgetProgress1 = tk.Label(budgetProgressFrame, text="Remaining", bg="green", width=40, height=2)
budgetProgress2 = tk.Label(budgetProgressFrame, text="Spent", bg="red", width=40, height=2)
budgetProgress1.grid(row=0, column=0)
budgetProgress2.grid(row=0, column=1)

budgetProgressFrame.grid(row=5, column=0, columnspan=2)


# updates a progress bar showing amount remaining vs spent
def updateBudgetProgress():
    totalBudget = 0
    totalSpent = 0
    
    for budget in data:
        if budget["type"] == "budget": # find all budgets, sum the total
            totalBudget += budget["amount"]
            for expense in data: # find all expenses for these budgets, sum the total
                if expense["type"] == "expense" and expense["category"] == budget["desc"]:
                    totalSpent += expense["amount"]
    try:
        if float(max(1-(totalSpent/totalBudget), 0)) == 0: # if the totalBudget has a width of 0 - setting width = 0 doesn't make the label invisible, it has a minimum width based on the text contents
            budgetProgress1.grid_forget() # forget the totalBudget label
            budgetProgress2.config(text="Spent", bg="red", width=40)
            budgetProgress2.grid(row=0, column=1)
       
        elif float(min(totalSpent/totalBudget, 1)) == 0: # if the totalSpent has a width of 0
            budgetProgress2.grid_forget() # forget the totalSpent label
            budgetProgress1.config(text="Remaining", bg="green", width=40)
            budgetProgress1.grid(row=0, column=0)
       
        else: # for when neither has a width of 0, assign them a length according to the ratio of remaining:spent
            budgetProgress1.config(text="Remaining", bg="green", width=int(40*float(max(1-(totalSpent/totalBudget),0)))) # remaining
            budgetProgress2.config(text="Spent", bg="red", width=int(40*float(min(totalSpent/totalBudget,1)))) # spent
            budgetProgress1.grid(row=0, column=0)
            budgetProgress2.grid(row=0, column=1)

    except ZeroDivisionError: # this occurs when no budgets set
        budgetProgress1.grid(row=0, column=0)
        budgetProgress1.config(width=40, text="No Budgets Set", bg="gray")
        budgetProgress2.grid_forget()





# reportFrame - lets you do smart forecasting, generate reports, budget alerts
reportFrame = tk.Frame(root)

# generate report, smart forecasting, budget alerts
generateReportButton = tk.Button(reportFrame, text="Generate Report", font=("Arial", 12), command=lambda:generateReport())
smartForecastingButton = tk.Button(reportFrame, text="Smart forecast", font=("Arial", 12), command=lambda:generateForecast())
showBudgetAlertButton = tk.Button(reportFrame, text="Show Budget Alerts", font=("Arial", 12), command=lambda:budgetReport())

reportLabel = tk.Label(reportFrame, text="", font=("Arial", 12))

# put everything on grid
generateReportButton.grid(row=0, column=0)
smartForecastingButton.grid(row=0, column=1)
showBudgetAlertButton.grid(row=0, column=2)

reportLabel.grid(row=1, column=0, columnspan=3)

#exit button
exitReportButton = tk.Button(reportFrame, text="Exit", font=("Arial", 12), command=lambda:showMainFrame())
exitReportButton.grid(row=2, column=0, columnspan=3)






#==============================================================================================
# Functions - The other functions, I don't know what to call them but they allow frame switching and button validation
#==============================================================================================
 # all functions to switch menus
 # could probably be combined into a single function, if we take the current frame as a parameter
def showMainFrame():
    transactionListbox.delete(0, tk.END)
    loadListbox()
    
    incomeFrame.pack_forget()
    expenseFrame.pack_forget()
    billFrame.pack_forget()
    budgetFrame.pack_forget()
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
    
def showBudgetFrame(): # reusing transactionListbox to show budgets when in this frame
    mainFrame.pack_forget()
    updateBudgetProgress()
    budgetFrame.pack()
    budgetProgressFrame.grid(row=5, column=0, columnspan=2)
    
    
    transactionListbox.delete(0, tk.END) # clears the listbox
    for x in data: # loops through the data to find budgets and adds them
        if x['type'] == "budget":
            transactionListbox.insert("end", f"{x['type']} - {x['date']} - £{x['amount']} for {x['desc']}")
    
    

def buttonval(): # prevents the user from adding things until all required fields have a valid entry
    #validates adding income
    if incomeFrame.winfo_ismapped(): # checks which frame is currently being shown
        if valid_date(incomeDateEntry.get()) and valid_amount(incomeEntry.get()) and valid_text(incomeSourceEntry.get()):
            confirmIncomeButton.config(state='active')
            incomeWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
            root.bind("<Return>", lambda event: add_income(datetime.now().strftime("%d/%m/%Y"), incomeEntry.get().lstrip('0'), incomeDescriptionEntry.get(), incomeSourceEntry.get(), taxableOption.get())) # allows user to press enter to add
        else:
            confirmIncomeButton.config(state='disabled')
            incomeWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
            root.unbind("<Return>") # removes ability to press enter to add when the fields are invalid

    #validates adding expenses
    elif expenseFrame.winfo_ismapped():
        if valid_date(expenseDateEntry.get()) and valid_amount(expenseEntry.get()) and valid_text(expenseCategoryEntry.get()):
            confirmExpenseButton.config(state='active')
            expenseWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
            root.bind("<Return>", lambda event: add_expense(datetime.now().strftime("%d/%m/%Y"), expenseEntry.get().lstrip('0'), expenseDescriptionEntry.get(), expenseCategoryEntry.get(), importanceOption.get()))
        else:
            root.unbind("<Return>")
            confirmExpenseButton.config(state='disabled')
            expenseWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
            
    elif billFrame.winfo_ismapped():
        if valid_date(billDateEntry.get()) and valid_amount(billAmountEntry.get()) and valid_num(billFrequencyEntry.get()) and valid_text(billDescriptionEntry.get()):
            confirmBillButton.config(state='active')
            billWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
            root.bind("<Return>", lambda event: add_bill(datetime.now().strftime("%d/%m/%Y"), billAmountEntry.get().lstrip('0'), billDescriptionEntry.get(), billFrequencyEntry.get()))
        else:
            confirmBillButton.config(state='disabled')
            billWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
            root.unbind("<Return>")
    
    elif budgetFrame.winfo_ismapped():
        if valid_date(budgetDateEntry.get()) and valid_amount(budgetAmountEntry.get()) and valid_text(budgetCategoryEntry.get()):
            confirmBudgetButton.config(state='active')
            budgetWarningLabel.config(text="Notice: All fields have a valid entry.", fg="Green")
            root.bind("<Return>", lambda event: add_budget(datetime.now().strftime("%d/%m/%Y"), budgetAmountEntry.get(), budgetCategoryEntry.get()))
        else:
            confirmBudgetButton.config(state='disabled')
            budgetWarningLabel.config(text="Notice: All fields must have a valid entry.", fg="Red")
            root.unbind("<Return>")
  
    root.after(10, buttonval)

buttonval()
showMainFrame()

root.mainloop()
