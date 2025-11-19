import os
from library.functions import calc_balance, financial_status
from library.classes import Budget

os.system('cls' if os.name == 'nt' else 'clear')

name = input("Enter your name: ")
os.system('cls' if os.name == 'nt' else 'clear')

print(f"Hey {name}, this is BudgetBuddy! Your personal Budgeting Assistant.")
income = float(input("Enter your monthly income (only numbers): "))

total_expenses = []
budgets = []

while True:
    category = input("\nEnter a budget category (ex: grocery, car): ").strip()
    budget_obj = Budget(category)

    budget_obj.add_expenses()
    total_expenses.append(budget_obj.get_expenses())
    budgets.append(budget_obj)

    more = input("\nDo you want to add another category? (yes/no): ").lower()
    if more != "yes":
        break

total = sum(total_expenses)
balance = calc_balance(income, total)
financial_status(balance)

for b in budgets:
    b.get_expenses_list()
