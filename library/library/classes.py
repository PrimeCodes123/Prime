import os

class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type.lower().strip()
        self.filename = f"{self.expense_type}.txt"
        self.expenses_dict = {}

        self.load_old_expenses()

    def load_old_expenses(self):
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, "r") as file:
            for line in file:
                if ":" in line:
                    item, cost = line.strip().split(":")
                    self.expenses_dict[item.strip()] = float(cost.strip())

    def add_expenses(self):
        while True:
            try:
                num_expenses = int(input(f"Enter number of {self.expense_type} expenses you want to add (integers only): "))
                break
            except:
                print("\n ** ERROR ** Enter integers only.\n")
        
        print('Enter each expense in the format: "Item Cost" (Example: Milk 10)')
        
        for i in range(num_expenses):
            while True:
                try:
                    item, cost = input(f"Enter expense #{i+1}: ").split()
                    self.expenses_dict[item] = float(cost)
                    break
                except:
                    print("\n** ERROR ** Wrong format. Use: Item Cost\n")

        self.write_to_file()
        
    def get_expenses(self):
        return sum(self.expenses_dict.values())
    
    def get_expenses_list(self):
        print(f"\nList of {self.expense_type} expenses:")
        for item, cost in self.expenses_dict.items():
            print(f"{item} : {cost}")

    def write_to_file(self):
        with open(self.filename, "w") as file:
            for item, cost in self.expenses_dict.items():
                file.write(f"{item}: {cost}\n")

            
