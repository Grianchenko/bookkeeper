import sys
# from datetime import datetime
from PySide6 import QtWidgets

from expanse_tab import Expense
from budget_tab import Budget
from categories_tab import Categories


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home bookkeeper')
        self.resize(800, 600)

        central_widget = QtWidgets.QTabWidget()
        central_widget.addTab(Expense(), 'Expenses')
        central_widget.addTab(Budget(), 'Budgets')
        central_widget.addTab(Categories(), 'Categories')

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
