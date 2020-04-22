import sys
from qt_expense import ExpenseList, CategoryList



class Menu:
    # Display a menu and interact to choices when run
    def __init__(self):
        self.expenselist = ExpenseList()
        self.categorylist = CategoryList()
        self.choices = {
            '1': self.show_expenses,
            '2': self.add_expense,
            '3': self.modify_expense,
            '4': self.add_category,
            '5': self.modify_category,
            '6': self.quit,
        }

    def display_menu(self):
        print(
            """
Expense Program Menu

1. Show all expenses
2. Add a new expense
3. Modify an expense
4. Add a category
5. Modify a category
6. Quit
"""
            )

    def run(self):
        # Display the menu and respond to choices
        while True:
            self.display_menu()
            choice = input('Select an option: ')
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print('{0} is not a valid choice'.format(choice))

    def show_expenses(self, expenses=None):
        if not expenses:
            expenses = self.expenselist.expenses
        for expense in expenses:
            print('{0} : {1} - {2} - {3} - {4} ----- {5}'.format(expense.id, expense.creation_date, self.categorylist.categories[int(expense.category) - 1].name, expense.description, expense.country, expense.amount))

    def show_categories(self, categories=None):
        if not categories:
            categories = self.categorylist.categories
        for category in categories:
            print('{0}: {1}'.format(category.id, category.name))

    def add_expense(self):
        amount = input('Enter the amount: ')
        print('Please see below list of categories: \n')
        self.show_categories()
        category = input ('\nSelect a category: ')
        description = input('Add a description: ')
        country = input('Add the country (optional): ')
        self.expenselist.new_expense(amount, description, country, category)

    def modify_expense(self):
        print('Please see below the list of expenses:')
        self.show_expenses()
        id = input('Select an Expense ID: ')
        amount = input('Insert the new amount (leave blank if unchanged): ')
        description = input('Insert the new des4cription (blank = unchanged): ')
        country = input('Insert the new country (blank, unchanged): ')
        self.show_categories()
        category = input('Insert a new category (blank, unchanged): ')
        self.expenselist.modify_expense(id, amount, description, country, category)
    
    def add_category(self):
        name = input('Please input the name of the category: ')
        self.categorylist.new_category(name)
        print('Your category has been added')
    
    def modify_category(self):
        print('Please see below list of categories: \n')
        self.show_categories()
        while True:
            category_id = input('Please input the category ID you want to change: ')
            category_num = int(category_id)
            if category_num:
                print('The category you want to change is: ', self.categorylist.categories[category_num - 1].name)
                name = input('Please input the new category name: ')
                self.categorylist.change_category(category_id, name)
                break
            else:
                print('The ID you input is not correct')
    
    def quit(self):
        print('Thank you for using our program today.')
        sys.exit()



            
