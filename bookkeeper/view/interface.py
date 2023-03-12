from PySide6 import QtWidgets

from bookkeeper.view.expense_tab import ExpenseTab
from bookkeeper.view.budget_tab import BudgetTab
from bookkeeper.view.categories_tab import CategoriesTab


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, exp_repo, cat_repo):
        super().__init__()
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo

        self.setWindowTitle('Home bookkeeper')
        self.resize(800, 600)

        self.central_widget = QtWidgets.QTabWidget()
        self.central_widget.addTab(ExpenseTab(self.exp_repo, self.cat_repo), 'Expenses')
        self.central_widget.addTab(BudgetTab(), 'Budgets')
        self.central_widget.addTab(CategoriesTab(self.cat_repo), 'Categories')

        self.setCentralWidget(self.central_widget)
