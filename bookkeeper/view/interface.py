from PySide6 import QtWidgets, QtCore
from datetime import datetime

from bookkeeper.view.expense_tab import ExpenseTab
from bookkeeper.view.budget_tab import BudgetTab
from bookkeeper.view.categories_tab import CategoriesTab


class MainWindow(QtWidgets.QMainWindow):
    exp_button_clicked = QtCore.Signal(int, str, str, datetime)
    cat_button_clicked = QtCore.Signal(str, str)
    bud_button_clicked = QtCore.Signal(str, int)

    def __init__(self, exp_repo, cat_repo, bud_repo):
        super().__init__()
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.bud_repo = bud_repo

        self.setWindowTitle('Home bookkeeper')
        self.resize(1280, 760)

        self.expense = ExpenseTab(self.exp_repo, self.cat_repo)
        self.budget = BudgetTab(self.exp_repo, self.bud_repo)
        self.category = CategoriesTab(self.cat_repo, self.exp_repo)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.expense)
        self.layout.addWidget(self.budget)
        self.layout.addWidget(self.category)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.category.new_cat.button_clicked.connect(self.expense.new_exp.set_cat_list)
        self.expense.new_exp.button_clicked.connect(self.budget.act_bud.set_data)
        self.budget.edit_bud.button_clicked.connect(self.budget.act_bud.set_data)
