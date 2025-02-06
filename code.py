import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog,
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox,QTabWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')

class BudgetExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Planner and Expense Monitor")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.budget_tab = QWidget()
        self.expenses_tab = QWidget()
        self.tabs.addTab(self.budget_tab, "Budget")
        self.tabs.addTab(self.expenses_tab, "Expenses")
        self.initBudgetTab()
        self.initExpensesTab()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def initBudgetTab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.budget_category_input = QLineEdit()
        self.budget_amount_input = QLineEdit()
        self.budget_add_button = QPushButton("Add Budget")
        self.budget_add_button.clicked.connect(self.addBudget)
        form_layout.addRow(QLabel("Category:"), self.budget_category_input)
        form_layout.addRow(QLabel("Amount:"), self.budget_amount_input)
        form_layout.addWidget(self.budget_add_button)
        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(2)
        self.budget_table.setHorizontalHeaderLabels(["Category", "Amount"])
        self.budget_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addLayout(form_layout)
        layout.addWidget(self.budget_table)
        self.budget_chart_button = QPushButton("Generate Budget Chart")
        self.budget_chart_button.clicked.connect(self.plotBudgetChart)
        layout.addWidget(self.budget_chart_button)
        self.budget_tab.setLayout(layout)

    def initExpensesTab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.expense_category_input = QLineEdit()
        self.expense_amount_input = QLineEdit()
        self.expense_add_button = QPushButton("Add Expense")
        self.expense_add_button.clicked.connect(self.addExpense)
        form_layout.addRow(QLabel("Category:"), self.expense_category_input)
        form_layout.addRow(QLabel("Amount:"), self.expense_amount_input)
        form_layout.addWidget(self.expense_add_button)
        self.expenses_table = QTableWidget()
        self.expenses_table.setColumnCount(2)
        self.expenses_table.setHorizontalHeaderLabels(["Category", "Amount"])
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addLayout(form_layout)
        layout.addWidget(self.expenses_table)
        self.expenses_chart_button = QPushButton("Generate Expenses Chart")
        self.expenses_chart_button.clicked.connect(self.plotExpensesChart)
        layout.addWidget(self.expenses_chart_button)
        self.expenses_tab.setLayout(layout)

    def addBudget(self):
        category = self.budget_category_input.text()
        amount = self.budget_amount_input.text()
        if category and amount:
            row_position = self.budget_table.rowCount()
            self.budget_table.insertRow(row_position)
            self.budget_table.setItem(row_position, 0, QTableWidgetItem(category))
            self.budget_table.setItem(row_position, 1, QTableWidgetItem(amount))
            self.budget_category_input.clear()
            self.budget_amount_input.clear()

    def addExpense(self):
        category = self.expense_category_input.text()
        amount = self.expense_amount_input.text()
        if category and amount:
            row_position = self.expenses_table.rowCount()
            self.expenses_table.insertRow(row_position)
            self.expenses_table.setItem(row_position, 0, QTableWidgetItem(category))
            self.expenses_table.setItem(row_position, 1, QTableWidgetItem(amount))
            self.expense_category_input.clear()
            self.expense_amount_input.clear()

    def plotBudgetChart(self):
        categories = []
        amounts = []
        for row in range(self.budget_table.rowCount()):
            category = self.budget_table.item(row, 0).text()
            amount = float(self.budget_table.item(row, 1).text())
            categories.append(category)
            amounts.append(amount)

        if categories and amounts:
            plt.figure(figsize=(8, 8))
            plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title('Budget Distribution')
            plt.show()

    def plotExpensesChart(self):
        budget_categories = []
        budget_amounts = []
        for row in range(self.budget_table.rowCount()):
            category = self.budget_table.item(row, 0).text()
            amount = float(self.budget_table.item(row, 1).text())
            budget_categories.append(category)
            budget_amounts.append(amount)

        expense_categories = []
        expense_amounts = []
        for row in range(self.expenses_table.rowCount()):
            category = self.expenses_table.item(row, 0).text()
            amount = float(self.expenses_table.item(row, 1).text())
            expense_categories.append(category)
            expense_amounts.append(amount)

        if budget_categories and budget_amounts and expense_categories and expense_amounts:
            budget_df = pd.DataFrame({'Category': budget_categories, 'Amount': budget_amounts})
            expenses_df = pd.DataFrame({'Category': expense_categories, 'Amount': expense_amounts})
            merged_df = pd.merge(budget_df, expenses_df, on='Category', how='left')
            merged_df.fillna(0, inplace=True)
            merged_df.set_index('Category', inplace=True)
            merged_df.plot(kind='bar', figsize=(12, 6))
            plt.title('Budget vs. Actual Expenses')
            plt.xticks(rotation=0, ha='right')
            plt.tight_layout()
            plt.ylabel('Amount')
            plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BudgetExpenseApp()
    window.show()
    sys.exit(app.exec_())
