FinTrack - Financial Tracker and Budget Forecaster

Dependencies - There are none, the only required modules are part of the Python Standard Library and do not require installation.

How to use:
After running the program for the first time, a data.json file will be created in the same folder. This file contains the entire transaction history, including income, expenses, bills, and budgets.
The large box at the top of the program contains the transaction history, it will display income, expenses and bills. When on the budget menu, it will instead display only budgets.
Below the transaction history is 5 buttons, which will lead to different menus. The function of each menu is described by the button.


[Add Income] allows you to add sources of income. It's required inputs are: Income, how much you made; Source, where the income came from; Date, the date the income was recieved; Taxable, whether the income is taxable or not.
Aside from these required inputs, it also has the optional Description entry.


[Add Expense] allows you to add expenses. It's required inputs are: Expense cost, how much you paid; Category, the category the expense belongs to, e.g. food; Date, the date you paid; Importance, where the expense was a need or a want.
Aside from these, it also has the optional Description entry.


[Add Bill] lets you to add a recurring bill. The required inputs are: Amount, how much you're paying; Description, where the bill is coming from; Date, the date you started paying the bill; Frequency, how often you will pay the bill.
Other than these inputs, there is also a [Calculate Due Date] button which will calculate the next time you have to pay that bill.


[Budgetting] lets you set view and set budgets. The required inputs are: Amount, how much the budget is; Category, what the budget is for; Date, the date the budget was set.
On this menu, there is also a progress bar. This progress bar will show you how much you have remaining across all budgets, as well as how much you've paid towards them.


On these four menus, there are shared [Add X] and [Delete Selected] buttons.
[Add X] will add an item to the data if the required inputs are valid. It can be substituted by the enter key.
[Delete Selected] will delete the selected item, regardless of if you're on the menu that that item would belong to.


[Generate Report], which has three menus allowing you to generate various reports.

[Generate Report] will display the total amount paid in expenses towards the needs and wants categories.
[Smart Forecast] will show your current balance, as well as your balance after a 30-day period, where bills will have been paid.
[Show Budget Alerts] will list all of the added budgets, as well as the amount paid towards them or how much overbudget you are.
