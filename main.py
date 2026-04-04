# --- Extra comments for team members ---
# could add edit/delete transactions
# go back feature
# could improve report visuals further

import json
import os
from datetime import datetime

FILE = "data.json"


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
class Transaction:
    def __init__(self, id, date, amount, desc):
        self._id = id
        self._date = date
        self._amount = amount
        self._desc = desc

    def display(self):
        return f"{self._date:<12} £{self._amount:<8} {self._desc}"


class Income(Transaction):
    def __init__(self, id, date, amount, desc, source):
        super().__init__(id, date, amount, desc)
        self.source = source

    def display(self):
        return f"[INCOME]  {super().display()} | {self.source}"


class Expense(Transaction):
    def __init__(self, id, date, amount, desc, category, importance):
        super().__init__(id, date, amount, desc)
        self.category = category
        self.importance = importance

    def display(self):
        return f"[EXPENSE] {super().display()} | {self.category} ({self.importance})"


class RecurringBill(Transaction):
    def __init__(self, id, date, amount, desc, frequency):
        super().__init__(id, date, amount, desc)
        self.frequency = frequency

    def display(self):
        return f"[BILL]    {super().display()} | {self.frequency}"


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


def get_amount():
    while True:
        try:
            x = float(input("Amount (£): "))
            if x >= 0:
                return x
            print("Must be positive")
        except:
            print("Enter a valid number")


def new_id(data):
    return len(data) + 1


# System
data = load_data()


def add_income():
    screen("Add Income")

    d = input("Date (DD/MM/YYYY): ")
    if not valid_date(d):
        print("Invalid date")
        return pause()

    amt = get_amount()
    desc = input("Description: ")
    src = input("Source: ")

    obj = Income(new_id(data), d, amt, desc, src)

    data.append({
        "type": "income",
        "id": obj._id,
        "date": obj._date,
        "amount": obj._amount,
        "desc": obj._desc,
        "source": obj.source
    })

    save_data(data)
    print("\n[+] Income added")
    pause()


def add_expense():
    screen("Add Expense")

    d = input("Date (DD/MM/YYYY): ")
    if not valid_date(d):
        print("Invalid date")
        return pause()

    amt = get_amount()
    desc = input("Description: ")
    cat = input("Category: ").lower()
    imp = input("Need or Want: ")

    if cat == "food":
        spent = sum(x["amount"] for x in data if x.get("category") == "food")
        if spent + amt > 200:
            print("\n[-] Food budget exceeded")

    obj = Expense(new_id(data), d, amt, desc, cat, imp)

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
    print("\n[+] Expense added")
    pause()


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