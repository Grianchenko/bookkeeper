# from datetime import datetime
from PySide6 import QtWidgets, QtCore

from bookkeeper.view.utils import LabeledInput, HistoryTable, LabeledBox


class ActiveBudgets(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rows = ('Day', 'Week', 'Month')
        self.columns = ('Paid', 'Limit')
        self.train_data = [['1241.41241', '5000'],
                           ['4332.111', '15000'],
                           ['6156.12', '50000']]
        self.table = HistoryTable(self.rows, self.columns)
        self.table.set_data(self.train_data)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Budgets'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class BudgetManager(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(str, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length_choice = LabeledBox('Category', ['day', 'week', 'month'])
        self.limit_input = LabeledInput('New budget', '1000')
        self.submit_button = QtWidgets.QPushButton('Update')
        self.submit_button.clicked.connect(self.submit)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Budget manager'))
        self.layout.addWidget(self.length_choice)
        self.layout.addWidget(self.limit_input)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def submit(self) -> None:
        try:
            self.button_clicked.emit(str(self.length_choice.box.currentText()),
                                     int(self.limit_input.input.text()))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')


class BudgetTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        act_bud = ActiveBudgets()
        edit_bud = BudgetManager()
        self.layout.addWidget(act_bud)
        self.layout.addWidget(edit_bud)
        self.setLayout(self.layout)
