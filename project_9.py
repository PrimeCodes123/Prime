import tkinter as tk
from library.classes import Budget
from library import functions  


root = tk.Tk()
root.title("BudgetBuddy - Your Personal Budgeting Assistant")
root.geometry("450x500")
root.configure(bg="#9d00ff")  
root["padx"] = 10
root["pady"] = 10


income = 0.0
budgets = {}          
current_category = None  

name_entry = None     
category_entry = None
expense_entry = None



def clear_root():
    """Remove all widgets from the root window."""
    for widget in root.winfo_children():
        widget.destroy()


def restart_app():
    """Reset everything and return to the name screen."""
    global income, budgets, current_category
    income = 0.0
    budgets.clear()
    current_category = None

    clear_root()
    show_name_screen()


def show_name_screen():
    """First screen: ask for the user's name."""
    global name_entry
    tk.Label(root, text="Enter your name:", bg="#9d00ff",
             fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Button(root, text="Next", command=get_name).pack(pady=10)


def get_name():
    """Handle name input and move to the income screen."""
    name = name_entry.get().strip()
    if not name:
        tk.Label(root, text="Please enter a name.", bg="#9d00ff", fg="yellow").pack()
        return

    clear_root()

    tk.Label(root, text=f"Hey {name}, this is BudgetBuddy!",
             bg="#9d00ff", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Enter your monthly income (only numbers):",
             bg="#9d00ff", fg="white").pack(pady=5)

    income_entry = tk.Entry(root)
    income_entry.pack(pady=5)

    tk.Button(
        root,
        text="Next",
        command=lambda: handle_income(income_entry.get())
    ).pack(pady=10)


def handle_income(income_value):
    """Store income and go to the first category screen."""
    global income
    try:
        income = float(income_value)
    except ValueError:
        tk.Label(root, text="⚠️ Please enter a valid number for income.",
                 bg="#9d00ff", fg="yellow").pack()
        return

    clear_root()
    show_category_setup_screen()


def show_category_setup_screen():
    """Screen to choose or create a category, then move to expenses for that category."""
    global category_entry

    tk.Label(root, text="Enter a budget category (e.g., Grocery, Car):",
             bg="#9d00ff", fg="white").pack(pady=10)

    category_entry = tk.Entry(root)
    category_entry.pack(pady=5)

    tk.Button(
        root,
        text="Start Category",
        command=start_category
    ).pack(pady=10)

    tk.Button(
        root,
        text="Calculate Balance Now",
        command=calculate_balance
    ).pack(pady=5)


def start_category():
    """Create/load a Budget object for the given category and go to its expense screen."""
    global current_category

    category_name = category_entry.get().strip()
    if not category_name:
        tk.Label(root, text="⚠️ Please enter a category name.",
                 bg="#9d00ff", fg="yellow").pack()
        return

    key = category_name.lower()


    if key not in budgets:
        budgets[key] = Budget(category_name)

    current_category = budgets[key]

    clear_root()
    show_expense_screen(category_name)


def show_expense_screen(category_name):
    """Screen where the user can add expenses for the current category."""
    global expense_entry

    tk.Label(root, text=f"Enter your {category_name} expenses:",
             bg="#9d00ff", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(root, text='Type and Cost (e.g., "Milk 10")',
             bg="#9d00ff", fg="white").pack(pady=5)

    expense_entry = tk.Entry(root)
    expense_entry.pack(pady=5)

    tk.Button(
        root,
        text="Add Expense",
        command=add_expense
    ).pack(pady=5)

    tk.Button(
        root,
        text="Done with this Category (Add Another)",
        command=go_to_new_category
    ).pack(pady=5)

    tk.Button(
        root,
        text="Calculate Balance",
        command=calculate_balance
    ).pack(pady=10)


def add_expense():
    """Parse 'Item Cost' from the expense entry and add it to the current Budget."""
    global current_category

    if current_category is None:
        tk.Label(root, text="⚠️ No active category.",
                 bg="#9d00ff", fg="yellow").pack()
        return

    text = expense_entry.get().strip()
    try:
        item, cost = text.split()
        cost = float(cost)
        current_category.expenses_dict[item] = cost
        current_category.write_to_file()

        tk.Label(root, text=f"Added {item} : ${cost:.2f}",
                 bg="#9d00ff", fg="white").pack()
        expense_entry.delete(0, "end")

    except Exception:
        tk.Label(root, text='⚠️ Wrong format. Use: Item Cost (e.g., "Milk 10")',
                 bg="#9d00ff", fg="yellow").pack()


def go_to_new_category():
    """Return to the category setup screen to allow the user to add another category."""
    clear_root()
    show_category_setup_screen()


def calculate_balance():
    """Compute total expenses and balance, display details for all categories."""
    if income == 0.0 and not budgets:
        clear_root()
        tk.Label(root, text="No data yet. Please enter at least income and one expense.",
                 bg="#9d00ff", fg="yellow").pack(pady=20)
        tk.Button(root, text="Restart", command=restart_app).pack(pady=10)
        return

    total_exp = sum(b.get_expenses() for b in budgets.values())
    balance = functions.calc_balance(income, total_exp)

    clear_root()

    tk.Label(root, text=f"Total Expenses: ${total_exp:.2f}",
             bg="#9d00ff", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(root, text=f"Remaining Balance: ${balance:.2f}",
             bg="#9d00ff", fg="white", font=("Arial", 12, "bold")).pack(pady=5)


    functions.financial_status(balance)

    tk.Label(root, text="Expense Breakdown:",
             bg="#9d00ff", fg="white", font=("Arial", 12, "underline")).pack(pady=(15, 5))

    
    if not budgets:
        tk.Label(root, text="(No expenses recorded.)",
                 bg="#9d00ff", fg="white").pack(pady=5)
    else:
        for cat_name, budget_obj in budgets.items():
            pretty_name = budget_obj.expense_type.capitalize()
            tk.Label(root, text=f"{pretty_name} Expenses:",
                     bg="#9d00ff", fg="#d0ff00", font=("Arial", 11, "bold")).pack(pady=(8, 2))

            if not budget_obj.expenses_dict:
                tk.Label(root, text="(No expenses added yet.)",
                         bg="#9d00ff", fg="white").pack()
            else:
                for item, cost in budget_obj.expenses_dict.items():
                    tk.Label(root, text=f"{item} : ${cost:.2f}",
                             bg="#9d00ff", fg="white").pack()

    tk.Button(root, text="Restart", command=restart_app).pack(pady=15)



show_name_screen()
root.mainloop()
