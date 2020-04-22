import datetime

# Initialise the variable for the expense IDs
last_id = 0
last_category_id = 0
default_country = 'Malta'

class Expense:
    # The single expense class represented in a ExpenseList
    def __init__(self, amount, description, country = default_country, category = ''):
        # Initialise an expense with some attributes and optional country and category
        self.amount = amount
        self.description = description
        self.creation_date = datetime.date.today()
        global last_id
        last_id = last_id + 1
        self.id = last_id
        self.country = country
        self.category = category

class ExpenseList:
    # Initialise the collection of expenses
    def __init__(self):
        # Initialise with an empty list
        self.expenses = []

    def _find_expense(self, expense_id):
        # Locate the expense with given ID
        for expense in self.expenses:
            if str(expense.id) == str(expense_id):
                return expense
        return None

    def new_expense(self, amount, description, country='', category=''):
        # Create a new expense and add it to the list
        self.expenses.append(Expense(amount, description, country, category))

    def modify_expense(self, expense_id, amount=None, description=None, country=None, category=None):
        # Find the Expense and change its content
        expense = self._find_expense(expense_id)
        if expense:
            if amount:
                expense.amount = amount
            if description:
                expense.description = description
            if country:
                expense.country = country
            if category:
                expense.category = category
            return True
        return False

class Category:
    # Create a category object    
    def __init__(self, name):
        self.name = name
        global last_category_id
        last_category_id = last_category_id + 1
        self.id = last_category_id

class CategoryList:
    # Create a new category list

    def __init__(self):
        self.categories = []

    def _find_category(self, category_id):
        # Locate the category with given ID
        for category in self.categories:
            if str(category.id) == str(category_id):
                return category
        return None

    def change_category(self, category_id, name):
        # Change the given category name
        category = self._find_category(category_id)
        if category:
            category.name = name
            return True
        return False
        
    def new_category(self, name):
        # Create a new category and add it to the category list
        self.categories.append(Category(name))

   
        
