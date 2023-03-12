import sys
# from datetime import datetime
from PySide6 import QtWidgets

from bookkeeper.view.expanse_tab import Expense
from bookkeeper.view.budget_tab import Budget
from bookkeeper.view.categories_tab import Categories


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, exp_repo, cat_repo):
        super().__init__()
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo

        self.setWindowTitle('Home bookkeeper')
        self.resize(800, 600)

        self.central_widget = QtWidgets.QTabWidget()
        self.central_widget.addTab(Expense(self.exp_repo, self.cat_repo), 'Expenses')
        self.central_widget.addTab(Budget(), 'Budgets')
        self.central_widget.addTab(Categories(), 'Categories')
        # self.central_widget.currentWidget().new_exp.button_clicked.connect(print('bbbb'))

        self.setCentralWidget(self.central_widget)
