import os, sys
from PyQt5 import QtWidgets, uic
from qt_expense import Expense, ExpenseList, Category, CategoryList

class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.ui_path = os.path.dirname(os.path.abspath(__file__))
        self.call = uic.loadUi(self.ui_path + "/main.ui")
        self.expenselist = ExpenseList()
        self.categorylist = CategoryList()

    def run(self):
        self.add_expense_layout()
        self.call.actionModify_an_Expense.triggered.connect(self.modify_expense_layout)
        self.call.actionNew_Expense.triggered.connect(self.add_expense_layout)
        self.call.actionShow_all_Expense.triggered.connect(self.show_expenses_layout)
        self.call.actionExit.triggered.connect(self.quit_function)
        # Final execution, to be kept at the bottom
        self.call.show()
        self.app.exec()

    def add_expense_layout(self):
        # Call the first stack to show add expense screen
        self.call.buttonBox.accepted.connect(self.add_expense)
        self.show_categories(1)
        self.call.stackedWidget.setCurrentIndex(0)
        self.call.buttonBox.rejected.connect(self.quit_function)
        self.call.stackedWidget.setCurrentIndex(0)
        self.call.listWidget1.setCurrentRow(0)


    def add_expense(self):
        # Call the Class function to actually create an expense
        amount = self.call.amount_input.text()
        description = self.call.description_input.text()
        country = self.call.country_input.text()
        category = self.call.listWidget1.currentItem().text()
        param_list = [amount, description, country, category]
        for i in param_list:
            if i == '':
                self.errorbox('All fields need to completed')
            else:
                if (amount.isdigit()):
                    self.expenselist.new_expense(amount, description, country, category)
                    self.call.amount_input.setText('')
                    self.call.description_input.setText('')
                    self.call.country_input.setText('')
                    break
                else:
                    self.errorbox('The amount you provided is not a number')

    def errorbox(self, error_message):
        errbox = QtWidgets.QMessageBox()
        errbox.setText(error_message)
        errbox.exec()

    def show_categories(self, index):
        # Print the list of categories in the listWidget
        jointlistwidg = 'listWidget' + str(index)
        self.listwidgetAttr = getattr(self.call, jointlistwidg)
        self.listwidgetAttr.clear()
        categories = self.categorylist.categories
        if not categories:
            categories.append('Generic')
        for category in categories:
            self.listwidgetAttr.addItem(category)

    def show_expenses(self, index, expenses=None):
        # Print the list of expenses in the listWidget
        jointexpensewidg = 'expenseWidget' + str(index)
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
        self.show_expenses(2) # index 2 as for all functions in stackedWidget 1
        self.show_categories(2)
        self.call.expenseWidget2.setCurrentRow(0) # preselect first row
        self.expensewidgetclicked(self.call.expenseWidget2.currentItem())
        self.call.expenseWidget2.itemClicked.connect(self.expensewidgetclicked)
        self.call.buttonBox_2.accepted.connect(self.modify_expense)
    
    def modify_expense(self):
        # call the Class function to actually modify the expense
        amount = self.call.amount_input_2.text()
        description = self.call.description_input_2.text()
        country = self.call.country_input_2.text()
        category = self.call.listWidget2.currentItem().text()
        expense_id = self.call.ID_label_2_desc.text()
        param_list = [amount, description, country, category]
        for i in param_list:        
            if i == '':
                self.errorbox('All fields need to be completed')
                break
            else:
                if (amount.isdigit()):
                    self.expenselist.modify_expense(expense_id, amount, description, country, category)
                    self.show_expenses(2) # Update the expense list after the expense has been modified
                    self.show_categories(2) # Update categories
                    self.category_selection(expense_id) # Update the category selection
                    break
                else:
                    self.errorbox('The amount you provided is not a number')
                    self.call.amount_input_2.setText('')

    def expensewidgetclicked(self, item):
        # Change the modify expense fields to show the selected expense
        index = item.text().split(' - ')
        expense = self.expenselist._find_expense(index[0])    
        self.call.amount_input_2.setText(expense.amount)
        self.call.description_input_2.setText(expense.description)
        self.call.country_input_2.setText(expense.country)
        self.call.ID_label_2_desc.setText(str(expense.id))
        self.category_selection(str(expense.id))
     
    def category_selection(self, expense_id):      
        # Select the right category on the listWidget, based on the class attribute
        expense = self.expenselist._find_expense(expense_id)
        all_items = []
        # Iterate all category list in the widget
        for x in range(self.call.listWidget2.count()):
            all_items.append(self.call.listWidget2.item(x))
        # Select the correspondent category
        for i in all_items:
            if i.text() == expense.category:
                self.call.listWidget2.setCurrentItem(i)
    
    def show_expenses_layout(self):
        # Shape the layout for the show expense stack
        self.call.stackedWidget.setCurrentIndex(2)
        total = 0
        category_count = {}
        self.call.expenseTableWidget.setRowCount(0)
        for expense in self.expenselist.expenses:
            amount = expense.amount
            category = expense.category
            if category in category_count:
                category_count[category] += int(expense.amount)
            else:
                category_count[category] = int(expense.amount)
            description = expense.description
            creation_date = expense.creation_date
            country = expense.country
            expense_id = expense.id
            numRows = self.call.expenseTableWidget.rowCount()
            self.call.expenseTableWidget.insertRow(numRows)
            self.call.expenseTableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(expense_id)))
            self.call.expenseTableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(creation_date)))
            self.call.expenseTableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(amount))
            self.call.expenseTableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(description))
            self.call.expenseTableWidget.setItem(numRows, 4, QtWidgets.QTableWidgetItem(category))
            self.call.expenseTableWidget.setItem(numRows, 5, QtWidgets.QTableWidgetItem(country))
            self.call.expenseTableWidget.resizeColumnsToContents()
            total = total + int(expense.amount)
        self.call.total_label_number.setText(str(total))
        self.call.categoryTableWidget.setRowCount(0)
        for category in category_count:
            numRows = self.call.categoryTableWidget.rowCount()
            self.call.categoryTableWidget.insertRow(numRows)
            self.call.categoryTableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(category))
            self.call.categoryTableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(category_count[category])))


    def quit_function(self):
        sys.exit()

if __name__ == '__main__':
    Main().run()

    