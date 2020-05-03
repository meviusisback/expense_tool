import os, sys
from PyQt5 import QtWidgets, uic, QtCore
from qt_expense import Expense, ExpenseList, Category

class Main:
    def __init__(self):
        # Initialise the UI
        self.app = QtWidgets.QApplication([])
        self.ui_path = os.path.dirname(os.path.abspath(__file__))
        self.call = uic.loadUi(self.ui_path + "/main.ui")
        # Creates the ExpenseList and the Category list objects
        self.expenselist = ExpenseList()
        # Toolbar Menu entries - File
        self.call.actionModify_an_Expense.triggered.connect(self.modify_expense_layout, QtCore.Qt.UniqueConnection)
        self.call.actionNew_Expense.triggered.connect(self.add_expense_layout, QtCore.Qt.UniqueConnection)
        self.call.actionShow_all_Expense.triggered.connect(self.show_expenses_layout, QtCore.Qt.UniqueConnection)
        self.call.actionCategories.triggered.connect(self.categories_layout, QtCore.Qt.UniqueConnection)
        self.call.actionExit.triggered.connect(self.quit_function, QtCore.Qt.UniqueConnection)
        self.call.buttonBox.rejected.connect(self.quit_function, QtCore.Qt.UniqueConnection)
        self.call.buttonBox.accepted.connect(self.add_expense, QtCore.Qt.UniqueConnection)
        self.call.buttonBox_2.accepted.connect(self.modify_expense, QtCore.Qt.UniqueConnection)
        self.call.buttonBox_2.rejected.connect(self.modify_expense_layout, QtCore.Qt.UniqueConnection)
        self.call.expenseWidget2.itemClicked.connect(self.expensewidgetclicked, QtCore.Qt.UniqueConnection)
        self.call.add_button.clicked.connect(self.add_categories, QtCore.Qt.UniqueConnection)
        self.call.modify_button.clicked.connect(self.modify_category, QtCore.Qt.UniqueConnection)
    


    def run(self):
        # First interface is for adding an expense
        self.add_expense_layout()
        
        # Final execution, to be kept at the bottom
        self.call.show()
        self.app.exec()

    def add_expense_layout(self):
        # Call the first stack to show add expense screen
        self.show_categories(1)
        self.call.stackedWidget.setCurrentIndex(0)
        self.call.listWidget1.setCurrentRow(0)


    def add_expense(self):
        # Call the Class function to actually create an expense
        amount = self.call.amount_input.text()
        description = self.call.description_input.text()
        country = self.call.country_input.text()
        category = self.call.listWidget1.currentItem().text()
        param_list = {
            'amount': amount,
            'description': description,
            'country': country,
            'category': category
        }
        if self.fields_check(param_list) == True:
            if (amount.isdigit()):
                self.expenselist.new_expense(amount, description, country, category)
                self.call.amount_input.setText('')
                self.call.description_input.setText('')
                self.call.country_input.setText('')
            else:
                self.errorbox('The amount you provided is not a number')
        
    
    def errorbox(self, error_message):
        # ErrorBox execution on the UI
        errbox = QtWidgets.QMessageBox()
        errbox.setText(error_message)
        errbox.exec()

    def show_categories(self, index):
        # Print the list of categories in the listWidget
        jointlistwidg = 'listWidget' + str(index)
        # Makes sure it selects the correct index for picking the right table
        self.listwidgetAttr = getattr(self.call, jointlistwidg)
        self.listwidgetAttr.clear()
        categories = self.expenselist.categories
        if not categories:
            self.expenselist.new_category('Generic')
        for category in categories:
            content_category = category.name
            self.listwidgetAttr.addItem(content_category)

    def show_expenses(self, index, expenses=None):
        # Print the list of expenses in the listWidget
        jointexpensewidg = 'expenseWidget' + str(index)
        # Makes sure it selects the correct index for picking the right table
        self.expensewidgetAttr = getattr(self.call, jointexpensewidg)
        self.expensewidgetAttr.clear()
        if not expenses:
            expenses = self.expenselist.expenses
        for expense in expenses:
            content_expense = str(expense.id) + ' - ' + expense.amount + ' - ' + expense.description
            self.expensewidgetAttr.addItem(content_expense)


    def modify_expense_layout(self):
        # Shape the layout for the modify expense stack
        self.call.stackedWidget.setCurrentIndex(1)
        # index 2 as for all functions in stackedWidget 1
        self.show_expenses(2) 
        self.show_categories(2)
        # Preselect first row
        self.call.expenseWidget2.setCurrentRow(0) 
        self.expensewidgetclicked(self.call.expenseWidget2.currentItem())
        
        
    
    def modify_expense(self):
        # call the Class function to actually modify the expense
        amount = self.call.amount_input_2.text()
        description = self.call.description_input_2.text()
        country = self.call.country_input_2.text()
        category_text = self.call.listWidget2.currentItem().text()
        category = self.expenselist._find_category(category_text)
        expense_id = self.call.ID_label_2_desc.text()
        param_list = {
            'amount': amount,
            'description': description,
            'country': country,
            'category': category
        }
        # After checking that all fields are not empty, check if amount is digit
        check_fields = self.fields_check(param_list)
        if check_fields == True:
            if (amount.isdigit()):
                self.expenselist.modify_expense(expense_id, amount, description, country, category)
                # Update the expense list after the expense has been modified
                self.show_expenses(2) 
                # Update categories
                self.show_categories(2) 
                # Makes sure the expense category is selected right
                expense = self.expenselist._find_expense(expense_id)
                self.category_selection(expense) 
            else:
                self.errorbox('The amount you provided is not a number')
                self.call.amount_input_2.setText('')

    def fields_check(self, param_list):
        # Checks that all fields sent to this function are not empty
        for parameter in param_list:
            if param_list[parameter] == '':
                self.errorbox('All fields need to be completed')
                return False
        return True    

    def expensewidgetclicked(self, item):
        # Changes the modify expense fields to show the selected expense
        # Collects the index from the UI item provided as argument
        if item:
            index = item.text().split(' - ')
            # Calls the find expense function in the ExpenseList class
            expense = self.expenselist._find_expense(index[0])    
            self.call.amount_input_2.setText(expense.amount)
            self.call.description_input_2.setText(expense.description)
            self.call.country_input_2.setText(expense.country)
            self.call.ID_label_2_desc.setText(str(expense.id))
            self.category_selection(expense)
     
    def category_selection(self, expense):      
        # Select the right category on the listWidget, based on the class attribute
        category = expense.category
        all_items = []
        # Iterate all category list in the widget
        for x in range(self.call.listWidget2.count()):
            all_items.append(self.call.listWidget2.item(x))
        # Select the correspondent category
        for i in all_items:
            if i.text() == category.name:
                self.call.listWidget2.setCurrentItem(i)
    
    def show_expenses_layout(self):
        # Shape the layout for the show expense stack
        self.call.stackedWidget.setCurrentIndex(2)
        # Initiate the total
        total = 0 
        category_count = {}
        self.call.expenseTableWidget.setRowCount(0)

        # Iterate all the expenses from the expenselist
        for expense in self.expenselist.expenses: 
            amount = expense.amount
            category = expense.category
            if category in category_count: 
                # Increase the category total amount
                category_count[category] += int(expense.amount)
            else:
                # Add the category to the list for category amount calculation
                category_count[category] = int(expense.amount) 
            description = expense.description
            creation_date = expense.creation_date
            country = expense.country
            expense_id = expense.id
            # Add a new row in the table for each expense
            numRows = self.call.expenseTableWidget.rowCount()
            self.call.expenseTableWidget.insertRow(numRows)
            self.call.expenseTableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(expense_id)))
            self.call.expenseTableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(creation_date)))
            self.call.expenseTableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(amount))
            self.call.expenseTableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(description))
            self.call.expenseTableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(category.name))
            self.call.expenseTableWidget.setItem(numRows, 5, QtWidgets.QTableWidgetItem(country))
            self.call.expenseTableWidget.resizeColumnsToContents()
            total = total + int(expense.amount)
        # Print the total amount of all expenses
        self.call.total_label_number.setText(str(total))
        self.call.categoryTableWidget.setRowCount(0)
        # Add the category counts to the UI
        for category in category_count:
            numRows = self.call.categoryTableWidget.rowCount()
            self.call.categoryTableWidget.insertRow(numRows)
            self.call.categoryTableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(category.name))
            self.call.categoryTableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(category_count[category])))

    def categories_layout(self):
        # Define the layout for the categories stack
        self.call.stackedWidget.setCurrentIndex(3)
        # Iterate the category list to list all categories
        self.category_show()
        self.call.categorieslistWidget.setCurrentRow(0)
        
    def category_show(self):
        # Refresh the category list in stack 3
        self.call.categorieslistWidget.clear()
        for category in self.expenselist.categories:
            # Add the number of expenses that have that category to the text string
            category_text = str(category.id) + ' - ' + category.name + ' - ' + str(self.count_expense_category(category))
            self.call.categorieslistWidget.addItem(category_text)
    
    def count_expense_category(self, category):
        # Count how many expenses have a specific category
        count = 0
        for expense in self.expenselist.expenses:
            if category == expense.category:
                count += 1
        return count

    def add_categories(self):
        # Add a new category to ExpenseList
        line_text = self.call.add_categories_line.text()
        if line_text == '':
            self.errorbox('Category field is empty')
            return False
        else:
            for category in self.expenselist.categories:
                if line_text == category:
                    self.errorbox('This category exists already')
                    return False
            else:
                self.expenselist.new_category(line_text)
                self.category_show()
                self.call.add_categories_line.setText('')

    def modify_category(self):
        item = self.call.categorieslistWidget.currentItem()
        item = item.text().split(' - ')
        inputbox = QtWidgets.QInputDialog()
        text, ok = inputbox.getText(self.call, 'Category Name', 'Please input the new category name: ', QtWidgets.QLineEdit.Normal, '')
        if ok and text:
            self.expenselist.change_category(int(item[0]), text)
            self.category_show()
            self.call.categorieslistWidget.setCurrentRow(0)

    def quit_function(self):
        sys.exit()

if __name__ == '__main__':
    Main().run()

    